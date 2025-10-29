class ListProduct:
    def __init__(self):
        self.products = []
    def add_product(self, p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)
    def desc_price_products(self):
        """
        :return: desc sorted list of products
        """
        sorted_products = self.products.copy()
        for i in range (len(sorted_products)):
            for j in range (len(sorted_products)):
                if sorted_products[i].price > sorted_products[j].price:
                    sorted_products[j].price = sorted_products[i].price
                    sorted_products[i].price = sorted_products[j].price
        return sorted_products

