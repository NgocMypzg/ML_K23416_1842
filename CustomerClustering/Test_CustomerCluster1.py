from CustomerClustering.CustomerCluster1 import getConnect, QueryDataset, showHistogram, elbowMethod, runKMeans, \
    visualizeKMeans, visualize3DKMeans

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '3141592653589793Mk.')

sql1 = 'select * from customer'
df1 = QueryDataset(conn, sql1)
print(df1.head())

sql2= """
select distinct customer.CustomerId, Age, Annual_Income, Spending_Score
from customer, customer_spend_score
where customer.CustomerId = customer_spend_score.CustomerId"""
df2 = QueryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual_Income', 'Spending_Score']

print(df2.head())
print(df2.describe())

showHistogram(df2, df2.columns[1:])

columns = ['Age', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 4
colors = ['red', 'green', 'blue', 'purple', 'black', 'pink', 'orange']

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2['cluster'] = labels

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending_Score",
                colors)
# Gom cụm theo Income và Spending Score
columns = ['Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 5

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2['cluster'] = labels
visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual_Income",
                "Spending_Score",
                colors)

# Gom cụm với Age, Annual Income, Spending Score
columns = ['Age','Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster = 6
y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2['cluster'] = labels
print(df2.head())

hover_data = df2.columns
visualize3DKMeans(df2, columns, hover_data, cluster)
