from algosdk.future import transaction
from algosdk.encoding import decode_address
from datetime import datetime
from pyteal import compileTeal, Mode
from modules.helpers.time import get_current_timestamp, get_future_timestamp_in_secs
from modules.helpers.utils import (
    compile_program,
    wait_for_confirmation,
    get_private_key_from_mnemonic,
)

import config.escrow as config

from beaker.application import Application
from beaker.client.application_client import ApplicationClient
from modules.clients.AlgodClient import Algod
from algosdk.atomic_transaction_composer import AccountTransactionSigner


def deploy_new(
    EscrowContractClass,
    deployer_address: str = config.account_a_address,
    deployer_mnemonic: str = config.account_a_mnemonic,
    buyer_address: str = config.account_b_address,
    seller_address: str = config.account_c_address,
    escrow_payment_1: int = config.escrow_payment_1,
    escrow_payment_2: int = config.escrow_payment_2,
    total_price: int = config.total_price,
    asa_id: int = config.stablecoin_ASA,
    inspection_start: int = int(get_current_timestamp()),
    inspection_end: int = int(get_future_timestamp_in_secs(60)),
    inspection_extension: int = int(get_future_timestamp_in_secs(90)),
    closing=int(get_future_timestamp_in_secs(300)),
    closing_extension=int(get_future_timestamp_in_secs(360)),
    foreign_apps=[],
    foreign_assets=[],
):

    deployer_address = config.account_a_address
    deployer_mnemonic = config.account_a_mnemonic
    buyer_address = config.account_b_address
    seller_address = config.account_c_address

    deployer_private_key = get_private_key_from_mnemonic(deployer_mnemonic)
    signer = AccountTransactionSigner(deployer_private_key)

    escrowContract = EscrowContractClass()
    app_client = ApplicationClient(
        client=Algod().getClient(),
        app=escrowContract,
        signer=signer,
    )

    # print("<- inspection_start ->", inspection_start)
    # print(datetime.fromtimestamp(inspection_start), ":inspection_start:")
    # print("<- inspection_end ->", inspection_end)
    # print(datetime.fromtimestamp(inspection_end), ":inspection_end:")

    res = app_client.create(
        glbl_creator=deployer_address,
        glbl_buyer=buyer_address,
        glbl_seller=seller_address,
        glbl_escrow_1=escrow_payment_1,
        glbl_escrow_2=escrow_payment_2,
        glbl_total=total_price,
        glbl_inspect_start_date=inspection_start,
        glbl_inspect_end_date=inspection_end,
        glbl_inspect_extension_date=inspection_extension,
        glbl_closing_date=closing,
        glbl_closing_extension_date=closing_extension,
        glbl_asa_id=asa_id,
        note="cashBuy__v1.0.0",
    )

    print("res[2] to get tx_id", res[2])

    tx_id = res[2]
    wait_for_confirmation(Algod.getClient(), tx_id)
    # display results
    transaction_response = Algod.getClient().pending_transaction_info(tx_id)
    # print("transaction_response", transaction_response)
    confirmed_round = transaction_response["confirmed-round"]

    print(f"deployed app_id: {app_client.app_id}")
    # print(f"Current app state: {app_client.get_application_state()}")

    print("compiling and dumping contract ABI...")
    escrowContract.dump("./build")

    return {
        "app_id": app_client.app_id,
        "confirmed_round": confirmed_round,
        "inspection_start": inspection_start,
        "inspection_end": inspection_end,
        "closing_date": closing
    }
