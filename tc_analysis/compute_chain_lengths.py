from binascii import hexlify

from ipv8.attestation.trustchain.database import TrustChainDB

day_stats = {}
database_path = u"/Users/martijndevos/Documents/trustchain-db"
db = TrustChainDB(database_path, "trustchain")
print("Database opened!")

users_info = db.execute("SELECT DISTINCT public_key, COUNT(*) FROM blocks GROUP BY public_key")
print("Fetch user info!")
with open("identities.csv", "w") as out_file:
    out_file.write("public_key,blocks\n")
    for user_info in users_info:
        out_file.write("%s,%d\n" % (hexlify(user_info[0]).decode(), user_info[1]))
