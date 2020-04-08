from binascii import hexlify, unhexlify

from deprecated.encoding import decode

from ipv8.attestation.trustchain.database import TrustChainDB

day_stats = {}
database_path = u"/Users/martijndevos/Documents/trustchain-db"
db = TrustChainDB(database_path, "trustchain")
print("Database opened!")

public_keys = []
balances = {}

# Load public keys
with open("chain_lengths.csv", "r") as in_file:
    did_header = False
    for line in in_file.readlines():
        if not did_header:
            did_header = True
            continue

        parts = line.split(",")
        public_key = unhexlify(parts[0])
        public_keys.append(public_key)

processed = 0
for public_key in public_keys:
    last_block = list(db.execute("SELECT tx, type FROM blocks WHERE public_key = ? ORDER BY block_timestamp DESC LIMIT 1", (public_key,)))[0]
    processed += 1

    if last_block[1] != b"tribler_bandwidth":
        print("NO BW %s" % last_block[1])
        continue

    decoded_tx = decode(last_block[0])[1]
    try:
        total_up = decoded_tx[b"total_up"]
        total_down = decoded_tx[b"total_down"]
        balances[public_key] = (total_up, total_down)
    except KeyError:
        print("Invalid tx: %s" % decoded_tx)

    if processed % 100 == 0:
        print("Processed %d keys..." % processed)

with open("balances.csv", "w") as out_file:
    out_file.write("public_key,total_up,total_down\n")
    for public_key, balance in balances.items():
        out_file.write("%s,%d,%d\n" % (hexlify(public_key).decode(), balance[0], balance[1]))
