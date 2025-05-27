import requests
import json
import csv
import time
import os

# Load config
with open("config.json") as f:
    config = json.load(f)

api_token = config["api_token"]
wallet_address = input("Enter a Bitcoin wallet address: ").strip()

# Prepare CSV output to output to the both tool directories for plotting later
output_file = os.path.join(os.path.dirname(__file__), "..", "data_analysis_tool", "trace_output.csv")
output_file = os.path.abspath(output_file)

    # open CSV file for writing and write header
with open(output_file, mode="w", newline="", encoding="utf-8") as f:

    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["tx_hash", "received_time", "from_address", "to_address", "value_btc"])

    # Get full transaction list for the wallet
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet_address}/full?token={api_token}"

    # Make the API request
    response = requests.get(url)

    # Check for errors in fetching data
    if response.status_code != 200:
        print(f"Error fetching wallet data: {response.status_code}")
        exit()
    
    # Parse the JSON response to get transactions
    wallet_data = response.json()

    # Check if the wallet has transactions
    transactions = wallet_data.get("txs", [])

    # Print the amount of transactions found
    print(f"Found {len(transactions)} transactions for wallet {wallet_address}")

    # Loop through each transaction
    for tx in transactions:

        # Extract transaction hash
        tx_hash = tx.get("hash")

        # Extract received time
        received_time = tx.get("received")

        # Input addresses
        inputs = []
        for i in tx.get("inputs", []):
            addr_list = i.get("addresses")
            if addr_list:
                inputs.extend(addr_list)
            else:
                inputs.append("N/A")


        # Output addresses
        outputs = tx.get("outputs", [])

        # Loop through each output address
        for out in outputs:

            # Check if the output address is not empty
            to_addr = out.get("addresses", ["N/A"])[0]

            # Check if the output address is the wallet address
            value_btc = out.get("value", 0) / 1e8

            # Loop through each input address
            for from_addr in inputs:

                # Write the transaction details to the CSV file
                writer.writerow([tx_hash, received_time, from_addr, to_addr, f'="{value_btc:.8f}"'])

        # Sleep to avoid hitting the API rate limit
        time.sleep(1)

# Print completion message
print(f"Export complete! Trace saved to: {output_file}")
