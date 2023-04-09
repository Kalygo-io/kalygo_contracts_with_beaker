from multiprocessing.dummy import Array
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
    AtomicTransactionComposer,
    TransactionWithSigner,
)
from algosdk.abi import Contract


def buyer_request_contract_updt(
    app_id: int,
    atc: AtomicTransactionComposer,
    abi: Contract,
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
):
    print(
        "Buyer Request Contract Update...",
        "sender",
        sender,
    )

    signer = AccountTransactionSigner(sender_private_key)

    # note = "for optin to stablecoin ASA".encode()
    # ptxn = transaction.PaymentTxn(sender, params, receiver, amount, None, note)
    # tws = TransactionWithSigner(ptxn, signer)

    atc.add_method_call(
        app_id,
        abi.get_method_by_name("buyer_request_contract_update"),
        sender,
        params,
        signer,
        method_args=[
            "E4S5DU5BXPHFSJI4D7DPR3L2EXSPTCHAHZFQEQIHE655N6GCM72YCKSMRA",  # buyer,
            "E4S5DU5BXPHFSJI4D7DPR3L2EXSPTCHAHZFQEQIHE655N6GCM72YCKSMRA",  # seller,
            100,  # escrowAmount1AsInt,
            200,  # escrowAmount2AsInt,
            300,  # escrowTotalAsInt,
            1678464673,  # IP start
            1678464773,  # IP end
            1678464873,  # IP ext
            1678465073,  # IP close
            1678465173,  # IP close ext
        ],
        boxes=[[app_id, "buyer_updt"], [app_id, "seller_updt"]],  # type: ignore
    )

    res = atc.execute(algod_client, 2)
