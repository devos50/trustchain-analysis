"""
This script creates datasets containing interactions between peers, based on the TrustChain dataset.
This output can be used to run experiments or simulations based on real-world data.
"""
import os
import shutil
from datetime import datetime

from ipv8.attestation.trustchain.database import TrustChainDB

from tc_analysis import DB_PATH

NUM_DATASETS = 1

block_creation_stats = []

db = TrustChainDB(DB_PATH, "trustchain")
print("Database opened!")

if not os.path.exists("identities.csv"):
    print("Identities not found!")
    exit(1)

# Determine the busiest days (e.g., most blocks created)
with open("creation_stats.csv") as stats_file:
    parsed_header = False
    for line in stats_file.readlines():
        if not parsed_header:
            parsed_header = True
            continue

        parts = line.strip().split(",")
        day = parts[0]
        num_blocks = int(parts[1])
        block_creation_stats.append((num_blocks, day))

block_creation_stats = sorted(block_creation_stats, reverse=True)

if os.path.exists("datasets"):
    shutil.rmtree("datasets", ignore_errors=True)
os.mkdir("datasets")

for dataset_index in range(NUM_DATASETS):
    identities_in_dataset = set()
    actions = []

    print("Will created dataset from day: %s (blocks: %d)" % (block_creation_stats[dataset_index][1], block_creation_stats[dataset_index][0]))
    day_parts = block_creation_stats[dataset_index][1].split("-")

    day_start_timestamp = (datetime(int(day_parts[2]), int(day_parts[1]), int(day_parts[0])) - datetime(1970, 1, 1)).total_seconds() * 1000
    day_end_timestamp = day_start_timestamp + (24 * 3600 * 1000)
    query = "SELECT public_key, link_public_key, block_timestamp FROM blocks WHERE block_timestamp >= %d AND block_timestamp <= %d ORDER BY block_timestamp" % (day_start_timestamp, day_end_timestamp)
    res = list(db.execute(query))
    print("Received blocks: %d" % len(res))
    for block_info in res:
        public_key, link_public_key, block_timestamp = block_info
        actions.append((public_key, link_public_key, block_timestamp - day_start_timestamp))
        identities_in_dataset.add(public_key)
        identities_in_dataset.add(link_public_key)

    # Convert the identities to numeric (peer) IDs
    identities_list = sorted(list(identities_in_dataset))
    identity_to_id = {}
    peer_id = 1
    for identity in identities_list:
        identity_to_id[identity] = peer_id
        peer_id += 1

    with open(os.path.join("datasets", "%d.txt" % (dataset_index + 1)), "w") as out_file:
        for (public_key, link_public_key, block_timestamp) in actions:
            out_file.write("%d,%d,%d\n" % (identity_to_id[public_key], identity_to_id[link_public_key], block_timestamp))

    print("Generated dataset with %d identities!" % len(identities_in_dataset))

print("Datasets generated!")
