from Review.product import Product
from Review.products import ListProduct

lp = ListProduct()
lp.add_product(Product(1, "Product 1", 50, 300000))
lp.add_product(Product(2, "Product 2", 60, 100000))
lp.add_product(Product(3, "Product 3", 90, 3007000))
lp.add_product(Product(4, "Product 4", 10, 30000))
lp.add_product(Product(5, "Product 15", 20, 30000))
lp.print_products()
for p in lp.desc_price_products():
    print(p)

