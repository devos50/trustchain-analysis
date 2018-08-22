"""
This script outputs the bandwidth balances of all users in the dataset
"""
from db.tc_database import TrustChainDB

database_path = u"/Users/martijndevos/Documents/py-ipv8/sqlite/trustchain.db"
db = TrustChainDB(database_path)

users = db.get_users(limit=1000000)
data = []
for user_info in users:
    bandwidth_blocks = db.get_latest_blocks(user_info["public_key"].decode('hex'), block_type='tribler_bandwidth', limit=1)
    if not bandwidth_blocks:
        continue
    last_block = bandwidth_blocks[0]
    data.append((user_info["public_key"], last_block.transaction["total_up"], last_block.transaction["total_down"]))

with open("balances.csv", "w") as output_file:
    output_file.write("pubkey,up,down\n")
    for balance in data:
        output_file.write("%s,%s,%s\n" % (balance[0], balance[1], balance[2]))
