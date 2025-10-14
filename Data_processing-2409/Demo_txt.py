import pandas as pd

df = pd.read_csv('../Datasets/SalesTransactions.txt', encoding='utf-8'
                 , dtype='unicode', sep = '\t', low_memory=False)
print(df)
# Dữ liệu dạng chữ --> unicode

