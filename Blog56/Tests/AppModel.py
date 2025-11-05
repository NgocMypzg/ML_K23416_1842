from Connectors.Connector import Connector
from Models.PurchaseMLModel import PurchaseMLModel

connector=Connector()
connector.connect()
pm=PurchaseMLModel(connector)
pm.execPurchaseHistory()

dfTransform=pm.processTransform()
print(dfTransform.head())
pm.buildCorrelationMatrix(dfTransform)