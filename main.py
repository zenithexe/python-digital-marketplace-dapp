from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

def line():
    print('-------------------------------')
    

# Client to Connect to Localnet
algorand = AlgorandClient.default_local_net()

# Import Dispenser from KMD
dispenser = algorand.account.dispenser()

# print("Dispenser Account :", dispenser)
# line()

# Create a algorand account
creator = algorand.account.random()
# creator.address


# Fund Creator Account
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information((creator.address)))
line()

# Creating an algorand standard asset
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="zenithgo",
        unit_name="zngo",
        manager=creator.address,
        clawback=creator.address, # It allow us to take token from other accounts if set to true. Note: can only be declared at the time of creation.
        freeze=creator.address,
    )
)

# extracting the Asset ID
asset_id = sent_txn["confirmation"]["asset-index"]



# Creating a Receiver Account
receiver = algorand.account.random()


# Fund Receiver Account
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver.address,
        amount=10_000_000
    )
)


# Sending Asset to Receiver
# asset_transfer = algorand.send.asset_transfer(
#     AssetTransferParams(
#         sender=creator.address,
#         receiver=receiver.address,
#         asset_id=asset_id,
#         amount=10,
#     )
# )

# ^^^^^ This will give error, the receiver must 'opt-in' to the token or asset.


# Start of Group Transaction
group_txn = algorand.new_group()

#opt in
group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver.address,
        asset_id=asset_id,
    )
)


group_txn.add_payment( #The receiver is paying algo for the asset token
    PayParams(
        sender=receiver.address,
        receiver=creator.address,
        amount=1_000_000
    )
)

group_txn.add_asset_transfer( #Transfering the Asset
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver.address,
        asset_id=asset_id,
        amount=10
    )
)


#Execute txn group
group_txn.execute()



# Print the Entire info from the Receiver Account
print(algorand.account.get_information(receiver.address))


#Print the amount of the asset the receiver account holds after the transactions
print('Receiver Acount ASset Balance :', algorand.account.get_information(receiver.address)['assets'][0]['amount'])

#Print the remaining balance of the creator account after the transactions
print("Creator Account Balance :", algorand.account.get_information(creator.address)['amount']) 