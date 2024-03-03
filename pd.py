import pandas as pd

# Sample data (replace this with your actual data)
data = {
    'vrunda': [
        {'Invoice Id': 'SHB/456/20', 'Seller': 'Surabhi Hardwares, Bangalore', 'CGST': 315.00, 'SGST': 315.00, 'Amount': 3500.00, 'Date': '20-Dec-20', 'Category': 'Some category'},
        {'Invoice Id': 'SHB/457/20', 'Seller': 'Another Seller', 'CGST': 200.00, 'SGST': 200.00, 'Amount': 2500.00, 'Date': '21-Dec-20', 'Category': 'Another category'}
    ],
    # Add data for other users as needed
}

# Convert data to DataFrame
df = pd.DataFrame()

for user, expenses in data.items():
    df_user = pd.DataFrame(expenses)
    df_user['User'] = user  # Add a 'User' column to identify the user
    df = pd.concat([df, df_user], ignore_index=True)

# Convert 'Date' column to datetime object
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

# Group by month and user, and calculate total expense amount for each month and user
monthly_expenses = df.groupby([df['Date'].dt.to_period('M'), 'User'])['Amount'].sum()

# Calculate total amount spent by user
total_amount_by_user = df.groupby('User')['Amount'].sum()

# Other insights (example)
average_monthly_expenses_by_user = df.groupby([df['Date'].dt.to_period('M'), 'User'])['Amount'].mean()

# Print results
print("Monthly Expense Amounts by User:")
print(monthly_expenses)
print("\nTotal Amount Spent by User:")
print(total_amount_by_user)
print("\nAverage Monthly Expenses by User:")
print(average_monthly_expenses_by_user)
