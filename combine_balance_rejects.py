"""
Combine the TrustChain balances and the exit node reject balances in one file, that can be plotted with R.
"""

with open("combined_tc_reject_balances.csv", "w") as out_file:
    out_file.write("type,balance\n")

    with open("balances.csv", "r") as tc_balances_file:
        parsed_header = False
        for line in tc_balances_file.readlines():
            if not parsed_header:
                parsed_header = True
                continue

            parts = line.strip().split(",")
            tc_balance = int(parts[1]) - int(parts[2])
            out_file.write("trustchain,%d\n" % tc_balance)

    with open("reject_events.txt", "r") as rejects_file:
        for line in rejects_file.readlines():
            reject_balance = int(line.strip().split(",")[1])
            out_file.write("reject,%d\n" % reject_balance)
