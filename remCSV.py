import pandas as pd

# Read the CSV file into a DataFrame
df_constructors = pd.read_csv('f1db_new/constructors.csv')

# Select the necessary columns
df_teamdriver = df_constructors[['ID']]
df_teamdriver.columns = ['teamID']

# Assign each row an ID
df_teamdriver.insert(0, 'ID', range(1, len(df_teamdriver) + 1))

# Add 'driverID' and 'season' columns (you might need to fill these with actual data)
df_teamdriver['driverID'] = None
df_teamdriver['season'] = None

# Write the DataFrame to a new CSV file
df_teamdriver.to_csv('f1db_new/teamdriver.csv', index=False)