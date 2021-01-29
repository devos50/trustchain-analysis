from deprecated.encoding import decode

from ipv8.attestation.trustchain.database import TrustChainDB

day_stats = {}
database_path = u"/Users/martijndevos/Documents/trustchain-db"
db = TrustChainDB(database_path, "trustchain")
print("Database opened!")

BATCH_SIZE = 500000
TOTAL_BLOCKS = 103149931
FIVE_MB = 5 * 1024 * 1024

size_frequencies = {}
under_5_mb_size_frequencies = {}

parsed_blocks = 0
while parsed_blocks < TOTAL_BLOCKS:
    blocks = list(db.execute("SELECT link_sequence_number, type, tx FROM blocks ORDER BY block_timestamp ASC LIMIT %d OFFSET %d" % (BATCH_SIZE, parsed_blocks)))
    for block in blocks:
        if block[1] != b"tribler_bandwidth":
            continue

        if block[0] == 0:  # Source block
            decoded_tx = decode(block[2])[1]
            download_mb = int(decoded_tx[b"down"] / 1024.0 / 1024.0)
            if download_mb not in size_frequencies:
                size_frequencies[download_mb] = 0
            size_frequencies[download_mb] += 1

            if decoded_tx[b"down"] <= FIVE_MB:
                raw_download_kb = int(decoded_tx[b"down"] / 1024.0)
                # Round down to nearest hundred
                download_kb = int(raw_download_kb / 100) * 100

                if download_kb not in under_5_mb_size_frequencies:
                    under_5_mb_size_frequencies[download_kb] = 0
                under_5_mb_size_frequencies[download_kb] += 1

    parsed_blocks += len(blocks)
    print("Parsed %d blocks" % parsed_blocks)

with open("transfer_sizes.csv", "w") as out_file:
    out_file.write("value,frequency\n")
    for mb_value, frequency in size_frequencies.items():
        out_file.write("%d,%d\n" % (mb_value, frequency))

with open("transfer_sizes_under_5mb.csv", "w") as out_file:
    out_file.write("value,frequency\n")
    for kb_value, frequency in under_5_mb_size_frequencies.items():
        out_file.write("%d,%d\n" % (kb_value, frequency))
