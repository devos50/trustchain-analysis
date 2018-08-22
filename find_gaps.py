"""
This script attempts to find gaps in the TrustChain dataset.
"""
from db.tc_database import TrustChainDB

database_path = u"/Users/martijndevos/Documents/py-ipv8/sqlite/trustchain.db"
db = TrustChainDB(database_path)

users = db.get_users(limit=1000000)
for user_info in users:
    pub_key = user_info["public_key"].decode('hex')
    lowest_unknown = db.get_lowest_sequence_number_unknown(pub_key)
    latest_block = db.get_latest(pub_key)
    if lowest_unknown != latest_block.sequence_number + 1:
        print "Public key: %s" % pub_key.encode('hex')
        print "Lowest unknown sequence number: %d" % lowest_unknown
        print "Latest known block: %d" % latest_block.sequence_number
