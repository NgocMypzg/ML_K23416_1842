from CustomerClustering.Bonus_Sakila import get_customers_by_film, get_customers_by_category, \
    cluster_customers_interest, elbow_customers_interest
from CustomerClustering.CustomerCluster1 import getConnect

conn = getConnect('localhost', 3306, 'sakila', 'root', '3141592653589793Mk.')
print("Phân loại khách hàng theo Tên phim ")
print(get_customers_by_film(conn).head())
print("Phân loại khách hàng theo category")
print(get_customers_by_category(conn).head())
print("Elbow Gom cụm khách hàng về mức độ quan tâm")
elbow_customers_interest(conn)
print("Gom cụm khách hàng về mức độ quan tâm")
print(cluster_customers_interest(conn, 4).head)
