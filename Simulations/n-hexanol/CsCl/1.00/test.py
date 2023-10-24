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
system = top.createSystem(nonbondedMethod=app.PME, ewaldErrorTolerance=0.0005, switchDistance=1*u.nanometer,
                          nonbondedCutoff=1.2*u.nanometers, constraints=app.HBonds, rigidWater=True, 
                          removeCMMotion=True)
 
