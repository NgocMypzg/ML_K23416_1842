# Input: df
# Ouput: top 3 sản phẩm bán ra nhưng có giá trị lớn nhất
import pandas as pd


def top3_product_maxvalue(df):
    # Tính giá trị cho từng sản phẩm
    df['ProductValue'] = df['UnitPrice'] * df['Quantity']*(1-df['Discount'])

    # Tính tổng giá trị theo ProductID
    product_totals = df.groupby('ProductID')['ProductValue'].sum()

    # Lấy top 3 sản phẩm có tổng giá trị cao nhất
    top3_products = product_totals.sort_values(ascending=False).head(3)

    return top3_products


df = pd.read_csv('../Datasets/SalesTransactions.csv')
result = top3_product_maxvalue(df)
print(f"Danh sách các sản phẩm top 3 giá trị là:", result)
