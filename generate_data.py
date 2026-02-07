import pandas as pd
import random

def create_mock_excel(filename="mock_financial_data.xlsx"):
    # 1. Create a list of sample merchants and types
    merchants = ["Amazon", "Starbucks", "Apple Store", "Unknown Shell Co.", "Global Casino Ltd", "Local Gas Station", "Luxury Watches Inc"]
    tx_types = ["Online Purchase", "Wire Transfer", "POS Swipe", "ATM Withdrawal"]

    data = []
    
    # 2. Generate 50 rows of data
    for i in range(50):
        txn_id = f"TXN-{1000 + i}"
        
        # Mix in some high-value "suspicious" amounts and low-value "normal" ones
        if i % 10 == 0:  # Every 10th transaction is a "High Risk" candidate
            amount = round(random.uniform(5000, 15000), 2)
            merchant = random.choice(["Unknown Shell Co.", "Global Casino Ltd", "Luxury Watches Inc"])
        else:
            amount = round(random.uniform(5, 500), 2)
            merchant = random.choice(["Amazon", "Starbucks", "Apple Store", "Local Gas Station"])
            
        data.append({
            "Transaction_ID": txn_id,
            "Amount": amount,
            "Merchant": merchant,
            "Type": random.choice(tx_types),
            "Location": random.choice(["London, UK", "New York, USA", "Dubai, UAE", "Unknown IP"])
        })

    # 3. Create DataFrame and Export to Excel
    df = pd.DataFrame(data)
    
    # Requires 'openpyxl' installed: pip install openpyxl
    df.to_excel(filename, index=False)
    print(f"✅ Success! Created {filename} with {len(df)} transactions.")

if __name__ == "__main__":
    create_mock_excel()