from bs4 import BeautifulSoup
with open("../Datasets/SalesTransactions.xml", 'r', encoding='utf-8') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')
UelSample = bs_data.find_all('UelSample')
print(UelSample)