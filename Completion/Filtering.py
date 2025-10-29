from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.]])
print(data)
print("-"*10)
cleaned = data.dropna() # Xoá tất cả các dòng có Nan
print(cleaned)
cleaned2=data.dropna(how='all') #Xoá tất cả các dòng có tất cả thuộc tính là Nan
print(cleaned2)

