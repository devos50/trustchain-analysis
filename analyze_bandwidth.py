"""
This script analyzes the bandwidth blocks in the TrustChain dataset.
"""
from db.tc_database import TrustChainDB

database_path = u"/Users/martijndevos/Documents/py-ipv8/sqlite/trustchain.db"
db = TrustChainDB(database_path)

print("Fetching bandwidth blocks...")
bandwidth_blocks = db.get_blocks_with_type('tribler_bandwidth')
print("Filtering bandwidth blocks...")
bandwidth_blocks = [block for block in bandwidth_blocks if block.link_sequence_number == 0]  # Only consider originator blocks
print("Sorting bandwidth blocks...")
bandwidth_blocks = sorted(bandwidth_blocks, key=lambda blk: blk.transaction["down"])

with open("block_bw_sizes.csv", "w") as output_file:
    for block in bandwidth_blocks:
        output_file.write("%s\n" % block.transaction["down"])
