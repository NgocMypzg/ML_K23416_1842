from CustomerClustering.CustomerCluster1 import getConnect, QueryDataset, showHistogram, elbowMethod, runKMeans, \
    visualizeKMeans, visualize3DKMeans, printClusterDetails

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
# Xuất danh sách
printClusterDetails(df2)
from flask import Flask, render_template_string

app = Flask(__name__)

def showClustersWeb(df, cluster_col='cluster'):
    clusters = sorted(df[cluster_col].unique())
    html = """
    <html>
    <head>
        <title>Customer Clusters</title>
        <style>
            body {font-family: Arial; margin: 20px;}
            h1 {color: #003366;}
            h2 {color: #2a4d69;}
            table {border-collapse: collapse; width: 100%; margin-bottom: 30px;}
            th, td {border: 1px solid #ccc; padding: 6px; text-align: center;}
            th {background-color: #f2f2f2;}
            .btn {padding: 6px 12px; margin: 5px; background-color: #2a4d69; color: white; border: none; cursor: pointer;}
        </style>
    </head>
    <body>
        <h1>Customer Clusters</h1>
    """
    for c in clusters:
        cluster_df = df[df[cluster_col] == c]
        html += f"<h2>Cluster {c}</h2>"
        html += cluster_df.to_html(index=False)
        html += f"""
            <form action="/cluster/{c}" method="get" style="display:inline;">
                <button class="btn">Xem cụm {c}</button>
            </form>
            <form action="/export/{c}" method="get" style="display:inline;">
                <button class="btn">Xuất cụm {c}</button>
            </form>
        """
    html += "</body></html>"
    return html


@app.route('/')
def home():
    return showClustersWeb(df2)
@app.route('/cluster/<int:cluster_id>')
def show_single_cluster(cluster_id):
    cluster_df = df2[df2['cluster'] == cluster_id]
    return f"""
    <html>
    <head>
        <title>Cluster {cluster_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
            }}
            h1 {{
                color: #003366;
                text-align: center;
                margin-bottom: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                background-color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #e0e0e0;
                color: #333;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                background-color: #2a4d69;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                transition: background-color 0.3s;
            }}
            .btn:hover {{
                background-color: #1e3a50;
            }}
            .container {{
                max-width: 1000px;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chi tiết cụm khách hàng {cluster_id}</h1>
            {cluster_df.to_html(index=False)}
            <a href="/" class="btn">Quay lại trang chính</a>
            <form action="/export/{cluster_id}" method="get" style="display:inline;">
                <button class="btn">Xuất cụm</button>
            </form>
        </div>
    </body>
    </html>
    """

from flask import send_file
import io

@app.route('/export/<int:cluster_id>')
def export_cluster(cluster_id):
    cluster_df = df2[df2['cluster'] == cluster_id]
    output = io.StringIO()
    cluster_df.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'cluster_{cluster_id}.csv'
    )
# Phân ra từng cụm trên web, xuất file
if __name__ == '__main__':
    app.run()