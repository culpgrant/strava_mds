import pandas as pd

data = {
    "order_id": [1, 2, 3, 4, 5],
    "customer_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "order_date": pd.to_datetime(
        ["2024-01-10", "2024-01-15", "2024-01-20", "2024-01-25", "2024-01-30"]
    ),
    "order_amount": [50.99, 120.50, 87.25, 39.99, 150.00],
}

df = pd.DataFrame(data)
print(df)
