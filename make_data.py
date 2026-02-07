import pandas as pd
import random

def generate_demo_data():
    data = []
    # Generate 100 rows
    for i in range(100):
        is_fraud = random.random() > 0.90  # 10% chance of being "high risk"
        
        if is_fraud:
            amount = random.uniform(11000, 50000) # High amount rule
            txn_type = "International Wire"
        else:
            amount = random.uniform(10, 500)
            txn_type = "Retail Purchase"
            
        data.append({
            "Transaction_ID": f"TXN-{1000+i}",
            "User_ID": f"USER-{random.randint(500, 600)}",
            "Amount": round(amount, 2),
            "Type": txn_type,
            "Merchant": random.choice(["Global Exchange", "Local Shop", "Casino-Online", "Amazon"]),
            "City": random.choice(["London", "Dubai", "New York", "Unknown"])
        })
    
    df = pd.DataFrame(data)
    df.to_csv("test_transactions.csv", index=False)
    print("✅ Success! 'test_transactions.csv' created.")

if __name__ == "__main__":
    generate_demo_data()