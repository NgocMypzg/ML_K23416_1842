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
        emp = Employee(dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[6], dataset[5])
        return emp

    def getAllEmployee(self):
        sql = ("select * from employee")
        dataset = self.fetchAll(sql)
        print(dataset)
        employees = []
        for emp in dataset:
            e = Employee(emp[0], emp[1], emp[2], emp[3], emp[4], emp[6], emp[5])
            employees.append(e)
        return employees

    def getDetailEmployee(self, id):
        sql = ("select * from employee "
               "where ID = %s")
        val = (id,)
        dataset = self.fetchOne(sql, val)
        if not dataset:
            return None
        emp = Employee(dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[6], dataset[5])
        return emp

    def insertOneEmployee(self, emp : Employee):
        sql = """
        INSERT INTO `employee`
        (
        `EmployeeCode`,
        `Name`,
        `Phone`,
        `Email`,
        `IsDeleted`,
        `Password`)
        VALUES
        (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s);
        """
        val = (emp.EmployeeCode, emp.Name, emp.Phone, emp.Email, emp.IsDeleted, emp.Password)
        result = self.insertOne(sql, val)
        return result

    def updateOneEmployee(self, emp : Employee):
        sql = """
        UPDATE `employee`
        SET
        `EmployeeCode` = %s,
        `Name` = %s,
        `Phone` = %s,
        `Email` = %s,
        `IsDeleted` = %s,
        `Password` = %s
        WHERE `ID` = %s;
        """
        val = (emp.EmployeeCode, emp.Name, emp.Phone, emp.Email, emp.IsDeleted, emp.Password, emp.ID)
        result = self.insertOne(sql, val)
        return result

    def deleteOneEmployee(self, id):
        sql = """
        DELETE FROM `employee`
        WHERE id = %s;
        """
        var = (id, )
        result = self.insertOne(sql, var)
        return result







