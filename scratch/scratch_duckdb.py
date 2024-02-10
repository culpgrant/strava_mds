import polars as pl

data = {
    "order_id": [1, 2, 3, 4, 5],
    "customer_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "order_amount": [50.99, 120.50, 87.25, 39.99, 150.00],
}

df = pl.DataFrame(data)

print(df)
