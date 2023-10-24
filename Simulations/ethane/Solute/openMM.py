# Imports
import sys
import os
import openmm as mm
from openmm import app
from openmm import unit as u
from mdtraj.reporters import XTCReporter

print('Loading initial configuration and toplogy')
pdb = app.PDBFile('Initial.pdb')
top = app.GromacsTopFile('Topology.top', periodicBoxVectors=pdb.topology.getPeriodicBoxVectors())

# Creating system
print('Creating OpenMM System')
system = top.createSystem(nonbondedMethod=app.NoCutoff, constraints=app.HBonds,
                          rigidWater=True, removeCMMotion=True)
        
# Temperature-coupling by leap frog (BAOAB) Langevin integrator (NVT)
integrator = mm.LangevinMiddleIntegrator(298.15*u.kelvin, 1.0/u.picoseconds, 1.0*u.femtoseconds)

platform = mm.Platform.getPlatformByName('CUDA')
properties = {'CudaPrecision': 'mixed', 'CudaDeviceIndex': '0'}

# Create the Simulation object
sim = app.Simulation(top.topology, system, integrator, platform, properties)

# Set the particle positions
sim.context.setPositions(pdb.positions)

# Minimize the energy
print('Minimizing energy')
sim.minimizeEnergy()
    
# Draw initial MB velocities
sim.context.setVelocitiesToTemperature(298.15*u.kelvin)

# Equlibrate simulation
print('Equilibrating...')
sim.step(500000)  # 500000*1 fs = 0.5 ns

# Set up the reporters
sim.reporters.append(app.StateDataReporter('output.dat', 10, totalSteps=1000000+500000,
    time=True, potentialEnergy=True, kineticEnergy=True, temperature=True, volume=True, density=True,
    remainingTime=True, speed=True, separator='	'))

# Set up trajectory reporter
sim.reporters.append(XTCReporter('trajectory.xtc', reportInterval=10, append=False))

# Run dynamics
print('Running dynamics! (NPT)')
sim.step(1000000)