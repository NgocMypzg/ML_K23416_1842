from numpy import nan as NA
import pandas as pd
data = pd.DataFrame([
    [1., 6.5, 3.],
    [2., NA, NA],
    [NA, NA, NA],
    [NA, 6.5, 3.],
    [3, 6.5, 3.],
    [4, 7.5, 7.],
    [5, 2.5, 3]]) # kiểm tra lấy trung bình theo hàng or cột
print(data)
print('-'*10)
cleaned = data.fillna(data.mean())
print(cleaned)
## slide 14 mỗi phương pháp xếp hạng cho 1 ví dụ: cơ sở lý thuyết + ví dụ (đổi data)
