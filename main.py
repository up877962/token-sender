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
                        logging.info(f"Transferring {balance['balance']} {token} from {account} to {recipient}")
                        wallet.transfer(recipient, balance['balance'], token, "test")
                    elif balance['symbol'] == token and float(balance['balance']) == 0:
                        logging.info(f"{balance['symbol']} balance is 0")

        except Exception as e:
            logging.error(f"Error transferring tokens for account {account}: {e}")


if __name__ == "__main__":
    accounts_keys = {
        "account1": os.getenv('TH'),
        "account2": os.getenv('NOTA'),
        "account3": os.getenv('DD'),
        "account4": os.getenv('CC'),
        "account5": os.getenv('LC'),
        "account6": os.getenv('MC')
    }
    tokens = ["DENAR", "ORI"]
    recipient = "pompeylad"

    transfer_tokens(accounts_keys, tokens, recipient)
