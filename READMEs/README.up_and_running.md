# Steps for getting up-and-running

- $ ./sandbox up
- $ ./sandbox enter algod
    - : cd /data
    - : ./scripts/escrow/generate_test_accounts.sh
    
- $ poetry shell
- $ poetry install

### PRO TIP you must make sure the `Python: Selected Interpreter` and make sure it is the same path as the poetry virtualenv