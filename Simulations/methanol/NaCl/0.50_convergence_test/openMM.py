# Imports
import sys
import os
import openmm as mm
from openmm import app
from openmm import unit as u
from mdtraj.reporters import XTCReporter

print('Loading initial configuration and toplogy')
pdb = app.PDBFile('Initial.pdb')
top = app.GromacsTopFile('Topology_stand_alone.top', periodicBoxVectors=pdb.topology.getPeriodicBoxVectors())

# Creating system
print('Creating OpenMM System')
system = top.createSystem(nonbondedMethod=app.PME, ewaldErrorTolerance=0.0005, switchDistance=1*u.nanometer,
                          nonbondedCutoff=1.2*u.nanometers, constraints=app.HBonds, rigidWater=True, 
                          removeCMMotion=True)
        
# Temperature-coupling by leap frog (BAOAB) Langevin integrator (NVT)
integrator = mm.LangevinMiddleIntegrator(298.15*u.kelvin, 1.0/u.picoseconds, 2.0*u.femtoseconds)

# Pressure-coupling by a Monte Carlo Barostat (NPT)
system.addForce(mm.MonteCarloBarostat(1*u.bar, 298.15*u.kelvin, 25))

platform = mm.Platform.getPlatformByName('CUDA')
properties = {'CudaPrecision': 'mixed', 'CudaDeviceIndex': '0'}

# Create the Simulation object
sim = app.Simulation(top.topology, system, integrator, platform, properties)

# Create a dictionary to store all forces
forces = {sim.system.getForce(index).__class__.__name__: sim.system.getForce(index) for index in range(sim.system.getNumForces())}

# Set the particle positions
sim.context.setPositions(pdb.positions)

# Minimize the energy
print('Minimizing energy')
sim.minimizeEnergy()
    
# Draw initial MB velocities
sim.context.setVelocitiesToTemperature(298.15*u.kelvin)

# Equlibrate simulation
print('Equilibrating...')
sim.step(500000)  # 500000*2 fs = 1.0 ns

# Set up the reporters
sim.reporters.append(app.StateDataReporter('output.dat', 100, totalSteps=50000000+500000,
    time=True, potentialEnergy=True, kineticEnergy=True, temperature=True, volume=True, density=True,
    remainingTime=True, speed=True, separator='	'))

# Set up trajectory reporter
sim.reporters.append(XTCReporter('trajectory.xtc', reportInterval=100, append=False))

# Run dynamics
print('Running dynamics! (NPT)')
sim.step(50000000)

# Print PME information
print('''
PARTICLE MESH EWALD PARAMETERS
Separation parameter: {}
Number of grid points along the X axis: {}
Number of grid points along the Y axis: {}
Number of grid points along the Z axis: {}
'''.format(*forces['NonbondedForce'].getPMEParametersInContext(sim.context)))
