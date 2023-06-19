import pandas as pd

# Read the CSV files into dataframes
df1 = pd.read_csv('BX-Book-Ratings.csv')
df2 = pd.read_csv('BX-Books.csv')
df3 = pd.read_csv('BX-Users.csv')

# Concatenate the dataframes
merged_df = pd.concat([df1, df2, df3], axis=0)

merged_df = merged_df.reset_index(drop=True)

merged_df.to_csv('merged_file.csv', index=False)