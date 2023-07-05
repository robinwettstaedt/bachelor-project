import random
from faker import Faker
import psycopg2

# Setup Faker
fake = Faker()

# Connect to your postgres DB
conn = psycopg2.connect(
    dbname="db",
    user="postgres",
    password="postgres",
    host="192.168.0.23"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# This script assumes that the Payments table schema is (id serial primary key, amount money, payment_date date)
for i in range(100000):  # Generate 100,000 rows
    amount = round(random.uniform(1, 1000), 2)  # Random amount between 1 and 1000 with 2 decimal places
    payment_date = fake.date_between(start_date='-1y', end_date='today')  # Random date within last year

    # Execute insert statement
    cur.execute(
        "INSERT INTO Payments (amount, payment_date) VALUES (%s::money, %s)",
        (str(amount), payment_date)
    )

    print(f"Inserted row {i + 1}")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
