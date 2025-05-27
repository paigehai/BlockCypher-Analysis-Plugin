import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load and clean the data from the CSV file, returning a DataFrame
def load_and_clean_data(filepath):
    
    # Load the CSV file
    df = pd.read_csv(filepath)

    # Preprocess the data and clean BTC value column for proper numeric conversion
    df['value_btc'] = (
        df['value_btc'].astype(str)
        .str.replace('="', '', regex=False)
        .str.replace('"', '', regex=False)
        .str.replace('=', '', regex=False)
    )

    # Remove any non-numeric characters from the value_btc column
    df['value_btc'] = pd.to_numeric(df['value_btc'], errors='coerce')

    # Convert received_time to datetime
    df['received_time'] = pd.to_datetime(df['received_time'], errors='coerce')

    return df

# Function to find all unique wallets that interacted with the target wallet
def unique_wallets(df, target_wallet):
    # Filter rows where the target wallet received BTC
    received_from = df[df['to_address'] == target_wallet]

    # Filter rows where the target wallet sent BTC
    sent_to = df[df['from_address'] == target_wallet]

    # Get unique sending wallets (who sent BTC to target)
    unique_senders = received_from['from_address'].nunique()

    # Get unique recipient wallets (who received BTC from target)
    unique_recipients = sent_to['to_address'].nunique()

    # Print summary
    print(f"Unique wallets that sent BTC to {target_wallet}: {unique_senders}")
    print(f"Unique wallets that received BTC from {target_wallet}: {unique_recipients}")

    # Create bar chart for unique wallets
    plt.figure(figsize=(6, 5))
    plt.bar(['Senders to Target', 'Recipients from Target'], [unique_senders, unique_recipients], color=['purple', 'pink'])

    # Set the title and labels
    plt.title(f"Unique Wallets Interacting with {target_wallet}", fontsize=10)
    plt.ylabel("Number of Unique Wallets")

    # Adjust the layout to prevent clipping of labels
    plt.tight_layout()

    # Save the bar chart as an image
    plt.savefig("unique_wallets_summary.png")


# Function to plot the transaction flow diagram
def plot_transaction_flow(df):
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges from the data
    for _, row in df.iterrows():
        from_addr = row['from_address']
        to_addr = row['to_address']
        value_btc = float(row['value_btc'])

        # Skip the edge if the BTC value is less than 0.00001
        if value_btc < 0.00001:
            continue

        # If the edge already exists, accumulate the BTC value
        if G.has_edge(from_addr, to_addr):

            # Accumulate the weight of the edge
            G[from_addr][to_addr]['weight'] += value_btc
        # If the edge does not exist, create it    
        else:
            G.add_edge(from_addr, to_addr, weight=value_btc)

    # Prepare edge labels (BTC values)
    edge_labels = {(u, v): f"{d['weight']:.4f} BTC" for u, v, d in G.edges(data=True)}

    # Draw the graph
    plt.figure(figsize=(15, 10))

    # Set the layout for the graph
    pos = nx.spring_layout(G, k=0.6)

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color="purple", node_size=2000, font_size=8, arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray', font_size=8)

    # Set the title
    plt.title("Bitcoin Transaction Flow Diagram", fontsize=8)

    # Adjust the layout to prevent clipping of labels
    plt.tight_layout()

    # Save the graph as an image
    plt.savefig("transaction_flow.png", dpi=300)


# Function to create a bar chart of sender addresses
def plot_sender_bar_chart(df):
    # Count the number of transactions for each sender address
    sender_counts = df['from_address'].value_counts()

    # Create a bar chart for the sender addresses
    plt.figure(figsize=(20, 8))

    # Set the color for the bars
    sender_counts.plot(kind='barh', color='purple')

    # Set the title and labels
    plt.title("Sender Address Transaction Counts", fontsize=10)
    plt.xlabel("Number of Transactions")
    plt.ylabel("Sender Address")

    # Set x and y ticks
    plt.xticks(rotation=60, fontsize=6)
    plt.yticks(fontsize=6)

    # Adjust the layout to prevent clipping of labels
    plt.tight_layout()

    # Save the bar chart as an image
    plt.savefig("bar_senders.png")


# Function to create a bar chart of receiver addresses
def plot_receiver_bar_chart(df):

    # Count the number of transactions for each recipient address
    receiver_counts = df['to_address'].value_counts()

    # Create a bar chart for the receiver addresses
    plt.figure(figsize=(30, 16))
    receiver_counts.plot(kind='barh', color='purple')

    # Set the title and labels
    plt.title("Receiver Address Transaction Counts", fontsize=10)
    plt.xlabel("Number of Transactions")
    plt.ylabel("Receiver Address")

    # Set x and y ticks
    plt.xticks(rotation=60)
    plt.yticks(fontsize=6)

    # Adjust the layout to prevent clipping of labels
    plt.tight_layout()

    # Save the bar chart as an image
    plt.savefig("bar_receivers.png")

# Function to create a pie chart of transaction values
def plot_transaction_value_pie_chart(df):

    # Count frequency of each unique transaction amount
    amount_counts = df['value_btc'].round(8).value_counts().sort_index()

    # Create a pie chart for transaction amounts
    plt.figure(figsize=(7, 7))
    plt.pie(amount_counts, labels=[f"{amt:.8f} BTC" for amt in amount_counts.index], autopct='%1.1f%%', startangle=140, textprops={'fontsize': 6})

    # Set the title and layout
    plt.title("Transaction Amount Distribution", fontsize=10)

    # Adjust the layout to prevent clipping of labels
    plt.tight_layout()

    # Save the pie chart as an image
    plt.savefig("pie_transaction_values.png")


# Main function to execute the analysis
def main():
    # Load and clean the data
    df = load_and_clean_data("trace_output.csv")

    # Prompt user for target wallet
    target_wallet = input("Enter the target wallet address: ").strip()

    # Generate visualizations and insights
    unique_wallets(df, target_wallet)
    plot_transaction_flow(df)
    plot_sender_bar_chart(df)
    plot_receiver_bar_chart(df)
    plot_transaction_value_pie_chart(df)

    # Print the saved charts
    print("All charts saved:")
    print("> unique_wallets_summary.png")
    print("> transaction_flow.png")
    print("> bar_senders.png")
    print("> bar_receivers.png")
    print("> pie_transaction_values.png")


# Main entry point
if __name__ == "__main__":
    main()
