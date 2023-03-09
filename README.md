# TLDR

This is a library of production-grade smart contracts built for the Algorand blockchain using the Beaker Framework.

## Up & Running

- poetry shell
- poetry install

## Concerning the tests directory

All tests are using the code in found in the modules folder as helper functions. The code in the modules folder aims to use as much dependency injection as possible and all the tests are designed to be ran with the pytest command.

## Useful commands

- poetry run deploy
- poetry run pytest
- poetry run compile
- python -m pytest -s
- python -m pytest -s tests/escrow/test_initial_state.py

## Generating Test Accounts

- ./sandbox enter algod

## Pylance could not be resolved ERROR

- (Ctrl+Shift+P)
- then select the Python: Select Interpreter
