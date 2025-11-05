import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import Index
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# Thống kê, khám phá
df = pd.read_csv('Data/USA_Housing.csv')
print("Head:\n",df.head())
print("Info: \n",df.info())
print("Describe: \n",df.describe())
sns.heatmap(df.corr(numeric_only=True))
plt.show()
# Train Model
X = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)

lm = LinearRegression()
lm.fit(X_train,y_train)

predictions = lm.predict(X_test)
pre1 = lm.predict(X_test.iloc[[0]])
print("Kết quả 1 = ", pre1)
pre2=lm.predict([[66774.995817,5.717143,7.795215,4.320000,36788.980327]])

print("kết quả 2 =",pre2)
# Đánh giá
print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)

print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))
# Save model
modelname="housingmodel.zip"
pickle.dump(lm, open(modelname, 'wb'))

# Load model
modelname="housingmodel.zip"
trainedmodel=pickle.load(open(modelname, 'rb'))
features=Index(['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms', 'Area Population'],
 dtype='object')
coeff_df = pd.DataFrame(trainedmodel.coef_, features,columns=['Coefficient'])
print(coeff_df)
# Test dự đoán
prediction=trainedmodel.predict([[66774.995817,5.717143,7.795215,4.320000,36788.980327]])
print("kết quả =",prediction)


