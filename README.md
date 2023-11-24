[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8307837.svg)](https://doi.org/10.5281/zenodo.8307837)

# Electronic notebook: Free-energy decomposition of salt effects on the solubilities of small molecules and the role of excluded-volume effects (GAFF/SPCE/Heyda)

This is supporting information for the scientific manuscript by _Hervø-Hansen et al._ (_Chem. Sci._, 2023, doi: [10.1039/D3SC04617F](https://doi.org/10.1039/D3SC04617F)) on the solvation free energy of alcohols and alkanes in various electrolyte solutions using the energy-representation theory of solvation in combination with all-atom simulations. All figures within the analysis are publication ready and can be reproduced by running the provided Jupyter notebooks (`.ipynb`). For running the simulation we recommend you clone the repository.

### Layout
- `PDB_files` PDB files for various chemical species utilized.
- `Simulations` Directory containing raw ermod results and processed results. The directory is also used for location of trajectories and corresponding analysis upon reproduction.
- `Force_fields` Directory containing force parameters files (in gromacs format) for the various chemical species utilized.
- `Figures` Directory containing publication ready figures and images imported in the Juypter notebooks.
- `Data` Directory containing processed data such as Setschenow coefficients along with its species and energetic decompositions, and RDFs.
- `Forcefield_generation.ipynb` Jupyter notebook for generating force field files in any format for arbitary molecules.
- `Simulations.ipynb` Jupyter notebook for running molecular dynamics simulations using OpenMM.
- `Analysis.ipynb` Jupyter notebook for analysis of simulations and production of publication ready figures.
- `environment.yml` Conda environment file to recreate the simulation environment. The environment most importantly contains Numpy, Scipy, OpenMM, OpenMMTools, parmed, mdtraj, and Packmol.

### Usage
To open the notebook, install Python via [Miniconda](https://conda.io/miniconda.html) and make sure all required packages are loaded by issuing the following terminal commands
```bash
   conda env create -f environment.yml
   conda activate CavityFormation
   jupyter-notebook
```

### License
This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
