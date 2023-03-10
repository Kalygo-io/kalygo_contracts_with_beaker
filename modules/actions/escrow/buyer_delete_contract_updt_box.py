from multiprocessing.dummy import Array
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
    AtomicTransactionComposer,
    TransactionWithSigner,
)
from algosdk.abi import Contract

def buyer_delete_contract_updt_box(
    app_id: int,
    atc: AtomicTransactionComposer,
    abi: Contract,
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
):
    print(
        "Buyer Delete Contract Update Box...",
        "sender",
        sender,
    )

    signer = AccountTransactionSigner(sender_private_key)

    # note = "for optin to stablecoin ASA".encode()
    # ptxn = transaction.PaymentTxn(sender, params, receiver, amount, None, note)
    # tws = TransactionWithSigner(ptxn, signer)

    atc.add_method_call(
        app_id,
        abi.get_method_by_name("buyer_delete_contract_updt_box"),
        sender,
        params,
        signer,
        method_args=[],
        boxes=[[app_id, "buyer_updt"]],  # type: ignore
    )

    res = atc.execute(algod_client, 2)
