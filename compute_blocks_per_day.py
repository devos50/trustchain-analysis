"""
This script outputs the bandwidth balances of all users in the dataset
"""
import datetime

from ipv8.attestation.trustchain.database import TrustChainDB

day_stats = {}
database_path = u"/Users/martijndevos/Documents/trustchain-db"
db = TrustChainDB(database_path, "trustchain")
print("Database opened!")

BATCH_SIZE = 500000
MAX_BLOCKS = -1

unconfirmed_txs = set()
unconfirmed_links = set()
tx_times = {}


def write_results():
    with open("creation_stats.csv", "w") as output_file:
        output_file.write("day,confirmed,unconfirmed\n")
        for day, info in day_stats.items():
            output_file.write("%s,%d,%d\n" % (day, info["confirmed"], info["unconfirmed"]))


parsed_blocks = 0
while True:
    blocks = list(db.execute("SELECT public_key, sequence_number, link_public_key, link_sequence_number, block_timestamp, type FROM blocks ORDER BY block_timestamp DESC LIMIT %d OFFSET %d" % (BATCH_SIZE, parsed_blocks)))
    if len(blocks) == 0 or (MAX_BLOCKS != -1 and parsed_blocks >= MAX_BLOCKS):
        break

    for block in blocks:
        if block[5] != b"tribler_bandwidth":
            continue

        date = datetime.datetime.fromtimestamp(block[4] / 1000)
        day = date.strftime("%Y-%m-%d")
        if day not in day_stats:
            day_stats[day] = {"unconfirmed": 0, "confirmed": 0}

        if block[3] == 0:  # Source block
            if (block[0], block[1]) in unconfirmed_links:
                day_stats[day]["confirmed"] += 1
                unconfirmed_links.remove((block[0], block[1]))
            else:
                tx_times[(block[0], block[1])] = day
                unconfirmed_txs.add((block[0], block[1]))
        else:  # Linked block
            if (block[2], block[3]) in unconfirmed_txs:
                tx_day = tx_times[(block[2], block[3])]
                day_stats[tx_day]["confirmed"] += 1
                unconfirmed_txs.remove((block[2], block[3]))
            else:
                unconfirmed_links.add((block[2], block[3]))

    parsed_blocks += len(blocks)
    print("Parsed %d blocks (unconfirmed txs: %d)" % (parsed_blocks, len(unconfirmed_txs)))

# Process unconfirmed transactions
for unconfirmed_tx in unconfirmed_txs:
    tx_day = tx_times[unconfirmed_tx]
    if tx_day not in day_stats:
        day_stats[tx_day] = {"unconfirmed": 0, "confirmed": 0}
    day_stats[tx_day]["unconfirmed"] += 1

write_results()
