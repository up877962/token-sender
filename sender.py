from beem import Hive
from beem.account import Account
from beem.transactionbuilder import TransactionBuilder
from beem.asset import Asset
import time

# Initialize Hive instance
hive = Hive(node="https://api.hive.blog")

# Dictionary of accounts and their corresponding keys
accounts_keys = {
    "account1": "active_key1",
    "account2": "active_key2",
    "account3": "active_key3",
    "account4": "active_key4",
    "account5": "active_key5",
    "account6": "active_key6"
}

# List of tokens to monitor
tokens = ["TOKEN_SYMBOL1", "TOKEN_SYMBOL2"]


# Function to check account for incoming tokens and transfer them
def transfer_tokens(token_symbols, accounts_keys):
    while True:
        for account_name, active_key in accounts_keys.items():
            try:
                hive = Hive(node="https://api.hive.blog", keys=[active_key])
                account = Account(account_name, blockchain_instance=hive)

                for token_symbol in token_symbols:
                    # Fetch account balances
                    balances = account.get_balances()

                    # Check for the specific token
                    if token_symbol in balances:
                        amount = balances[token_symbol]
                        if amount > 0:
                            # Create transaction to transfer tokens
                            tx = TransactionBuilder(blockchain_instance=hive)
                            tx.add_operation(
                                hive.transfer(
                                    from_account=account_name,
                                    to_account="recipient_account",
                                    amount=amount,
                                    asset=Asset(token_symbol, blockchain_instance=hive)
                                )
                            )
                            # Sign and broadcast the transaction
                            tx.sign()
                            tx.broadcast()
                            print(f"Transferred {amount} {token_symbol} from {account_name} to recipient_account")
            except Exception as e:
                print(f"Error transferring tokens from {account_name}: {e}")

        # Wait for a few seconds before checking again
        time.sleep(10)


# Example usage
transfer_tokens(tokens, accounts_keys)
