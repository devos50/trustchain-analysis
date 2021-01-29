"""
This script outputs a CSV file with the number of confirmed and unconfirmed blocks per day.
"""
from ipv8.attestation.trustchain.database import TrustChainDB

from tc_analysis import DB_PATH

db = TrustChainDB(DB_PATH, "trustchain")
print("Database opened!")


query = "select strftime('%d-%m-%Y', block_timestamp/1000, 'unixepoch'), COUNT(*) from blocks group by strftime('%d-%m-%Y', block_timestamp/1000, 'unixepoch') ORDER BY block_timestamp"
res = list(db.execute(query))
creation_info = []
for day_info in res:
    creation_info.append(day_info)

print("Writing statistics")
with open("creation_stats.csv", "w") as output_file:
    output_file.write("day,blocks\n")
    for day, num_blocks in creation_info:
        output_file.write("%s,%d\n" % (day.decode(), num_blocks))
