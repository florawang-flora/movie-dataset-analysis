import pandas as pd
df = pd.read_csv('src/keywords.csv')
print(df.duplicated().sum())
print(df.duplicated(subset=['id']).sum())
print(df.duplicated()])
print(df.drop_duplicated()])
d