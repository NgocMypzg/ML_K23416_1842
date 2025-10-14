from RetailProject.Connectors.Connector import Connector
from RetailProject.Models.Employee import Employee


class Employee_Connector(Connector):
    def login(self, email, pwd):
        sql = ("select * from employee "
               "where Email=%s and Password=%s")
        val = (email, pwd)
        dataset = self.fetchOne(sql, val)
        if not dataset:
            return None
        emp = Employee(dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[6])
        return emp

