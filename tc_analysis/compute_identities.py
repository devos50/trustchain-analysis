"""
This script outputs a CSV file with identities and the number of blocks created for each identity.
"""
from binascii import hexlify

from ipv8.attestation.trustchain.database import TrustChainDB

from tc_analysis import DB_PATH

day_stats = {}
db = TrustChainDB(DB_PATH, "trustchain")
print("Database opened!")

users_info = db.execute("SELECT DISTINCT public_key, COUNT(*) FROM blocks GROUP BY public_key")
print("Fetched user info!")
user_id = 1
with open("identities.csv", "w") as out_file:
    out_file.write("id,public_key,blocks\n")
    for user_info in users_info:
        out_file.write("%d,%s,%d\n" % (user_id, hexlify(user_info[0]).decode(), user_info[1]))
        user_id += 1
