from datetime import datetime
from binascii import unhexlify

from ipv8.attestation.trustchain.database import TrustChainDB

public_keys = []
balances = {}
days_freq = {}

# Load public keys
with open("identities.csv", "r") as in_file:
    did_header = False
    for line in in_file.readlines():
        if not did_header:
            did_header = True
            continue

        parts = line.split(",")
        public_key = unhexlify(parts[0])
        public_keys.append(public_key)

database_path = u"/Users/martijndevos/Documents/trustchain-db"
db = TrustChainDB(database_path, "trustchain")
print("Database opened!")

none_first_blocks = 0
processed = 0
for public_key in public_keys:
    if processed % 1000 == 0:
        print("Processed %d keys..." % processed)

    first_block = db.get(public_key, 1)
    if not first_block:
        none_first_blocks += 1
    else:
        block_timestamp = first_block.timestamp // 1000
        block_time = datetime.fromtimestamp(block_timestamp)
        block_day = block_time.strftime("%Y-%m-%d")
        if block_day not in days_freq:
            days_freq[block_day] = 0
        days_freq[block_day] += 1

    processed += 1

# Write the block days
with open("new_identities_per_day.csv", "w") as out_file:
    out_file.write("day,new_identities\n")
    for day, freq in days_freq.items():
        out_file.write("%s,%d\n" % (day, freq))
