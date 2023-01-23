from pyteal import abi

from beaker.client import ApplicationClient
from beaker.application import Application
from beaker.decorators import external
from beaker import sandbox

class Calculator(Application):
    @external
    def add(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        """Add a and b, return the result"""
        return output.set(a.get() + b.get())

    @external
    def mul(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        """Multiply a and b, return the result"""
        return output.set(a.get() * b.get())

    @external
    def sub(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        """Subtract b from a, return the result"""
        return output.set(a.get() - b.get())

    @external
    def div(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        """Divide a by b, return the result"""
        return output.set(a.get() / b.get())

def main():
    # calc = Calculator()
    # print(calc.approval_program)
    # print(calc.clear_program)
    # print(json.dumps(calc.contract.dictify()))
    # Here we use `sandbox` but beaker.client.api_providers can also be used
    # with something like ``AlgoNode(Network.TestNet).algod()``
    algod_client = sandbox.get_algod_client()

    acct = sandbox.get_accounts().pop()

    # Create an Application client containing both an algod client and app
    app_client = ApplicationClient(
        client=algod_client, app=Calculator(), signer=acct.signer
    )

    # Create the application on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")