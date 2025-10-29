from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as  plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()

        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = database

        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connect.Error as error:
        print("Error =", error)
    return None

def closeConnection(conn):
    if conn!=None:
        conn.close()

def QueryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    return df

def showHistogram(df, columns):
    plt.figure(figsize = (7,8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
        sns.histplot(df[column], bins=32)
        plt.title(f"Histogram of {column}")
    plt.show()
def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertias = []
    for n in range(1, 11):
        model = KMeans(n_clusters = n,
                       init = 'k-means++',
                       max_iter = 500,
                       random_state= 42)
        model.fit(X)
        inertias.append(model.inertia_)
    plt.figure(1, figsize = (15,6))
    plt.plot(range(1, 11), inertias, 'o')
    plt.plot(range(1, 11), inertias, '-', alpha = 0.5)
    plt.xlabel('Number of clusters'), plt.ylabel('Cluster sum of squared distances')
    plt.show()

def runKMeans(X, cluster):
    model = KMeans(n_clusters = cluster,
                   init = 'k-means++',
                   max_iter = 500,
                   random_state= 42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize = (10,10))
    for i in range (cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s = 100,
                    c = colors[i],
                    label = "Cluster %i"%(i+1))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def visualize3DKMeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df,
                        x = columns[0],
                        y = columns[1],
                        z = columns[2],
                        color = "cluster",
                        hover_data = hover_data,
                        category_orders={'cluster': range(0, cluster)})
    fig.update(margin = dict(l = 0, r = 0, b = 0, t = 0))
    fig.show()