from CustomerClustering.CustomerCluster1 import QueryDataset, runKMeans, elbowMethod


def get_customers_by_film(conn):
    sql = """
    SELECT
        f.title AS film_title,
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    ORDER BY f.title, c.customer_id;
    """
    df = QueryDataset(conn, sql)
    return df

def get_customers_by_category(conn):
    sql = """
    SELECT DISTINCT
        cat.name AS category,
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    ORDER BY cat.name, c.customer_id;
    """
    df = QueryDataset(conn, sql)
    return df

def elbow_customers_interest(conn):
    sql = """
    SELECT
        c.customer_id,
        COUNT(r.rental_id) AS total_rentals,
        COUNT(DISTINCT i.film_id) AS unique_films,
        COUNT(DISTINCT fc.category_id) AS unique_categories,
        COUNT(DISTINCT r.inventory_id) AS unique_inventory
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_category fc ON i.film_id = fc.film_id
    GROUP BY c.customer_id;
    """
    df = QueryDataset(conn, sql)
    features = ['total_rentals', 'unique_films', 'unique_categories', 'unique_inventory']
    elbowMethod(df, features)

def cluster_customers_interest(conn, cluster):
    sql = """
    SELECT
        c.customer_id,
        COUNT(r.rental_id) AS total_rentals,
        COUNT(DISTINCT i.film_id) AS unique_films,
        COUNT(DISTINCT fc.category_id) AS unique_categories,
        COUNT(DISTINCT r.inventory_id) AS unique_inventory
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_category fc ON i.film_id = fc.film_id
    GROUP BY c.customer_id;
    """
    df = QueryDataset(conn, sql)
    features = ['total_rentals', 'unique_films', 'unique_categories', 'unique_inventory']
    X = df.loc[:, features].values
    y_kmeans, centroids, labels = runKMeans(X, cluster)
    print(y_kmeans)
    print(centroids)
    print(labels)
    df['cluster'] = labels
    return df['cluster']



