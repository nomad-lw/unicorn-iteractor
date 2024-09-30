from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.aerial.tx import Transaction, SigningCfg
from rest_client import send_json_payload
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend

from dotenv import load_dotenv
import os
import sys
import base64

# startup
load_dotenv()
if os.getenv('MNEMONIC') is None:
    raise ValueError("MNEMONIC environment variable is not set or is empty")

MNEMONIC: str = os.getenv('MNEMONIC')  # type: ignore

# constants
config = {
    "uwu_mainnet": NetworkConfig(
        chain_id="unicorn-420",
        url="rest+https://rest.unicorn.meme",
        fee_minimum_gas_price=7000,
        fee_denomination="uwunicorn",
        staking_denomination="uwunicorn",
    )
}

def load_wallet(mnemonic: str):
    return LocalWallet.from_mnemonic(mnemonic,"unicorn")

def get_unicorn_balances(address: str):
    # connect to network
    ledger_client: LedgerClient = LedgerClient(config["uwu_mainnet"])

    # load and print coin balances
    balances = ledger_client.query_bank_all_balances(Address(address))
    print(f"Balances for {address}:\n")
    for coin in balances:
        print(f'{coin.amount} ${coin.denom}')

def transfer_unicorn(target_addr: str|Address, amount: int, memo: str|None = None):
    target_addr = Address(target_addr)
    sam = load_wallet(MNEMONIC)
    print(f"Transferring {amount} UWU to {target_addr} from {sam.address()}...")

    ledger = LedgerClient(config["uwu_mainnet"])
    account = ledger.query_account(sam.address()) # sequence, acc_number
    print(f"Account: {account}")
    tx = Transaction()
    tx.add_message(MsgSend(
            from_address=str(sam.address()),
            to_address=str(target_addr),
            amount=[{"amount": str(amount), "denom": "uwunicorn"}],
        ))
    tx.seal(
        SigningCfg.direct(sam.public_key(), account.sequence),
        fee="1000uwunicorn",
        gas_limit=95000,
        memo=memo,
    )
    tx.sign(sam.signer(), config["uwu_mainnet"].chain_id, account.number)
    tx.complete()
    tx_bytes=tx.tx.SerializeToString()
    mode="BROADCAST_MODE_SYNC"

    txb = base64.b64encode(tx_bytes).decode("utf-8")
    print(f"tx_bytes: {txb}")
    gas_limit, fee = ledger.estimate_gas_and_fee_for_tx(tx)
    tx.seal(
        SigningCfg.direct(sam.public_key(), account.sequence),
        fee=fee,
        gas_limit=gas_limit,
        memo=memo,
    )
    print(f"Recalculated gas_limit: {gas_limit}, fee: {fee}")
    print(send_json_payload(payload={"tx_bytes": txb, "mode":"BROADCAST_MODE_SYNC" }))
    print("Done")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [..options]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "balance":
        if len(sys.argv) != 3:
            print("Usage: python script.py balance <address>")
            sys.exit(1)
        address = sys.argv[2]
        get_unicorn_balances(address)
    elif command == "transfer":
        if len(sys.argv) < 4 or len(sys.argv) > 5:
            print("Usage: python script.py transfer <target_addr> <amount> [memo]")
            sys.exit(1)
        target_addr = sys.argv[2]
        amount = int(sys.argv[3])
        memo = sys.argv[4] if len(sys.argv) == 5 else None
        transfer_unicorn(target_addr, amount, memo)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
