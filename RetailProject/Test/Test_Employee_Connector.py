from RetailProject.Connectors.Employee_Connector import Employee_Connector

empc = Employee_Connector()
emp = empc.login("ngocmy@gmail.com", "123")
if emp is None:
    print("Employee Connector Login Failed")
else:
    print("Employee Connector Login Succeeded")
    print(emp)