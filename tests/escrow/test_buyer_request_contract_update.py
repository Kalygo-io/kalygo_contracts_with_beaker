import pytest
import json
from modules.actions.escrow.fund_minimum_balance import fund_minimum_balance
from modules.actions.escrow.buyer_request_contract_updt import buyer_request_contract_updt
from modules.actions.escrow.deploy_new import deploy_new
from modules.actions.escrow.delete_contract import delete_contract

from algosdk import logic
import base64
from contracts.escrow.contract import ContractUpdate, EscrowContract
from algosdk.abi import Contract, ABIType
from algosdk.encoding import encode_address
import config.escrow as config
from modules.actions.escrow.withdraw_balance import withdraw_balance
from modules.actions.escrow.buyer_delete_contract_updt_box import buyer_delete_contract_updt_box
from modules.helpers.utils import (
    format_app_global_state,
    get_private_key_from_mnemonic,
)
from algosdk import constants
from modules.helpers.time import get_current_timestamp, get_future_timestamp_in_secs
from modules.clients.AlgodClient import Algod
from modules.clients.IndexerClient import Indexer

from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
)

from modules.helpers.get_txn_params import get_txn_params

record_codec_for_contract_update = ABIType.from_string(str(ContractUpdate().type_spec()))

@pytest.fixture(scope="module")
def escrow_contract():
    print()
    print()
    print("deploying escrow contract...")

    deployed_contract = deploy_new(
        EscrowContract,
        config.account_a_address,  # deployer_address
        config.account_a_mnemonic,
        config.account_b_address,  # buyer_address
        config.account_c_address,
        config.escrow_payment_1,  # escrow_payment_1
        config.escrow_payment_2,
        config.total_price,  # total_price
        config.stablecoin_ASA,
        int(get_current_timestamp()),  # Inspection Period Start Date
        int(get_future_timestamp_in_secs(60)),  # Inspection Period End Date
        int(get_future_timestamp_in_secs(90)),  # Inspection Period Extension Date
        int(get_future_timestamp_in_secs(120)),  # Moving Date
        int(get_future_timestamp_in_secs(240)),  # Closing Date
        int(get_future_timestamp_in_secs(360)),  # Free Funds Date
    )
    yield deployed_contract["app_id"]
    print()
    # print("tear down in fixture", deployed_contract["app_id"])
    # delete_contract(
    #     EscrowContract,
    #     deployed_contract["app_id"],
    #     config.account_a_mnemonic,
    # )


def test_buyer_request_contract_update(escrow_contract):
    app_id = escrow_contract
    # app_info = Algod.getClient().application_info(app_id)
    app_address = logic.get_application_address(app_id)
    algod_client = Algod.getClient()

    print('app_address', app_address)
    app_logs = Indexer.getClient().application_logs(app_id)
    print('app_logs PRE', app_logs)

    buyer_address = config.account_b_address
    buyer_private_key = get_private_key_from_mnemonic(config.account_b_mnemonic)

    # --- --- --- --- ---
    atc_0 = AtomicTransactionComposer()
    txn_params = get_txn_params(algod_client)
    fund_minimum_balance(
        atc_0,
        algod_client,
        txn_params,
        buyer_address,
        buyer_private_key,
        app_address,
        212100
    )
    # --- --- --- --- ---

    res = algod_client.account_info(app_address)
    print(">>> contract balance >>>", res["amount"])
    # assert res["amount"] == 112100

    # --- --- --- --- ---

    with open("build/contract.json") as f:
        js = f.read()
    ABI = Contract.from_json(js)

    atc_1 = AtomicTransactionComposer()
    txn_params = get_txn_params(algod_client, constants.MIN_TXN_FEE, 1)

    buyer_request_contract_updt(
        app_id,
        atc_1,
        ABI,
        algod_client,
        txn_params,
        sender=buyer_address,
        sender_private_key=buyer_private_key
    )

    print("_>_>_ _>_>_", res["amount"])

    res = algod_client.application_boxes(app_id)
    print(algod_client.application_boxes(app_id))
    for box in res["boxes"]:
        print("box", box)
        box_name = base64.b64decode(box["name"]).decode("utf-8")
        print("box key:", box_name)

        if box_name == 'buyer_updt':
            print('YAY')
            print("box key:", box_name)
            box_value = algod_client.application_box_by_name(
                app_id, bytes(box_name, "utf-8")
            )["value"]

            print('box_value', box_value)

            # record_codec_for_contract_update
            membership_record = record_codec_for_contract_update.decode(box_value)

            # print(membership_record)
            # print(f"\t{(box_name)} => {membership_record} ")
        # else:
            # print("box key:", box_name)
            # box_value = algod_client.application_box_by_name(
            #    app_id, bytes(box_name, "utf-8")
            # )["value"]
            # print(
            #     "box value:",
            #     base64.b64decode(box_value).decode("utf-8"),
            # )

    # atc_2 = AtomicTransactionComposer()
    # txn_params = get_txn_params(algod_client, constants.MIN_TXN_FEE, 1)

    # buyer_delete_contract_updt_box(
    #     app_id,
    #     atc_2,
    #     ABI,
    #     algod_client,
    #     txn_params,
    #     sender=buyer_address,
    #     sender_private_key=buyer_private_key
    # )

    # atc_3 = AtomicTransactionComposer()
    # withdraw_balance(
    #     app_id, atc_3, ABI, algod_client, txn_params, buyer_address, buyer_private_key
    # )

    # res = algod_client.account_info(app_address)

    # print("_>_>_ _>_>_", res["amount"])

    # assert res["amount"] == 0

    # app_logs = Indexer.getClient().application_logs(app_id)
    # print('app_logs POST', app_logs)
