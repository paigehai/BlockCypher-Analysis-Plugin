# Data Extraction Tool
This script fetches the full transaction history of a given Bitcoin wallet address using the BlockCypher API. It structures the transaction data into a CSV file for further analysis or visualisation.

## Setup Instructions
Ensure you have the required package installed using the root-level `dependencies.py`.
Add your API token to a `config.json` file:
{
  "api_token": "YOUR_API_TOKEN"
}

## Usage
cd transaction_tracer_tool
python transaction_trace.py

Enter the selected Bitcoin wallet when prompted
This transaction will be saved to /data_analysis_tool/trace_output.csv

## Output Format (CSV)
| tx\_hash | received\_time | from\_address | to\_address | value\_btc |
| -------- | -------------- | ------------- | ----------- | ---------- |

Each row represents one transaction output with a value in Bitcoin, linked from each input address.

## Notes 
The transaction extraction script respects API limits by sleeping between requests
The CSV output has been specifically formatted for compatibility with other custom analysis scripts
Ensure paths between the two tools are preserved to tool functions as expected.
BlockCypher API has a limit of 50 requests for free accounts, so ensure you are considering this when extracting information.

# License
This project is licensed under the [MIT License](https://opensource.org/license/mit).

# Acknowledgements
BlockCypher API
Python Open-Source Community (requests, networkx, matplotlib, pandas)