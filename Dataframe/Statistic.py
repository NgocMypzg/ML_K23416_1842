import pandas as pd
def find_orders_within_range(df, MinValue, MaxValue):
    # Tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum(),
        include_groups=False
    )
    # Lọc đơn hàng
    orders_within_range = order_totals[(order_totals >= MinValue) & (order_totals <= MaxValue)]
    # Danh sachs cac ma don hang khong trung nhau
    unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().to_list()
    return unique_orders
df = pd.read_csv('../Datasets/SalesTransactions.csv')
minValue = float(input("Nhập giá trị min:"))
maxValue = float(input("Nhập giá trị max:"))
result = find_orders_within_range(df, minValue, maxValue)
print(f"Danh sách các hoá đơn nằm trong phạm vi từ {minValue} đến {maxValue} là:", result)
