from beemgraphenebase.base58 import base58decode, base58encode
from hiveengine.wallet import Wallet
from beem import Steem
from beem.nodelist import NodeList
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def transfer_tokens(accounts_keys, tokens, recipient):
    nodelist = NodeList()
    nodelist.update_nodes()

    total_transferred = {token: 0.0 for token in tokens}

    for account, active_key in accounts_keys.items():

        logging.info(f"Processing account: {account}")

        try:
            stm = Steem(node=nodelist.get_hive_nodes(), keys=[active_key])
            account_obj = stm.wallet.getAccountFromPrivateKey(active_key)
            wallet = Wallet(account_obj, steem_instance=stm)
        except Exception as e:
            logging.error(f"Error setting up wallet for account {account}: {e}")
            continue

        try:
            balances = wallet.get_balances()
            for token in tokens:
                for balance in balances:
                    if balance['symbol'] == token and float(balance['balance']) > 0:
                        amount = float(balance['balance'])
                        logging.info(f"Transferring {amount} {token} from {account} to {recipient}")
                        wallet.transfer(recipient, amount, token, "test")
                        total_transferred[token] += amount
                    elif balance['symbol'] == token and float(balance['balance']) == 0:
                        logging.info(f"{balance['symbol']} balance is 0")

        except Exception as e:
            logging.error(f"Error transferring tokens for account {account}: {e}")

    for token, total in total_transferred.items():
        logging.info(f"Total {token} transferred to {recipient}: {total}")


if __name__ == "__main__":
    # dict of accounts, with desired output name and the active key from env vars
    accounts_keys = {
        "theholder": os.getenv('TH'),
        "notanotherone": os.getenv('NOTA'),
        "dogsdoodahs": os.getenv('DD'),
        "cantcount": os.getenv('CC'),
        "littlecount": os.getenv('LC'),
        "massivecount": os.getenv('MC')
    }

    tokens = ["DENAR", "ORI"]  # tokens to check and send
    recipient = "pompeylad"  # maximum of 16 chars

    transfer_tokens(accounts_keys, tokens, recipient)
