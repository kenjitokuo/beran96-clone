# beran96-clone

Verification data and Python scripts for the Beran superposition algebra associated with the 96 binary Beran operations.

## Purpose

This repository accompanies the paper on a Post-style completeness criterion for full OML term clone generation via Beran operations.

The repository reproduces the finite verification results used in the paper:

- the ternary superposition table for the 96 Beran operations;
- the closed subalgebras of the Beran superposition algebra;
- the 17 maximal proper subalgebras;
- the 9 maximal proper subalgebras containing the two binary projections;
- the 3 synchronization obstructions;
- the closure sizes for example bases.

## Repository structure

- `data/`: input data for the 96 Beran operations.
- `src/`: Python scripts.
- `logs/`: generated CSV output files and source verification data.
- `tests/`: regression tests for the main numerical claims.

## Main output files

- `logs/beran_composition_table.csv`
- `logs/closed_subalgebras.csv`
- `logs/maximal_obstructions.csv`
- `logs/projection_obstructions.csv`
- `logs/synchronization_obstructions.csv`
- `logs/example_basis_closures.csv`
- `logs/example_smid_beran_numbers.csv`
- `logs/verification_summary.csv`

The file `logs/beran_closed_algebras_with_minimum_generator_summary.csv` is the source closed algebra data used to construct `logs/closed_subalgebras.csv`.

## Reproduction

Run the following commands from the repository root.

    python src\build_composition_table.py
    python src\normalize_closed_subalgebras.py
    python src\extract_maximal_obstructions.py
    python src\write_synchronization_obstructions.py
    python src\write_example_basis_closures.py
    python src\write_example_smid_numbers.py
    python src\write_verification_summary.py
    python -m pytest -q

Expected test result:

    6 passed

## Verified numerical claims

The regression tests fix the following claims:

- number of closed subalgebras: 21748;
- number of maximal proper subalgebras: 17;
- maximal proper subalgebras by type: 4 block, 10 shadow, 3 synchronization;
- number of projection-containing maximal proper subalgebras: 9;
- projection-containing maximal proper subalgebras by type: 2 block, 4 shadow, 3 synchronization;
- `nand_basis` generates all 96 binary Beran operations;
- `complete_binary_basis` generates all 96 binary Beran operations;
- `shadow_meet_basis` is not full.

## Python version

The scripts were tested with Python 3.14.

