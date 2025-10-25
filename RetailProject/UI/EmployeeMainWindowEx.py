from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from RetailProject.Connectors.Employee_Connector import Employee_Connector
from RetailProject.Models.Employee import Employee
from RetailProject.UI.EmployeeMainWindow import Ui_MainWindow


class EmployeeMainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.empc = Employee_Connector()
        self.is_completed = True

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.displayEmployeeIntoTable()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def displayEmployeeIntoTable(self): # do hàm tự chạy khi có sự thay đổi dữ liệu
        if not self.is_completed:
            return
        self.employees = self.empc.getAllEmployee()
        # Remove existing data
        self.tableWidget_ListEmp.setRowCount(0)
        # Loading emp into table
        for employee in self.employees:
            # Get the last row (for appending):
            row = self.tableWidget_ListEmp.rowCount()
            # Insert a new row (at the last row):
            self.tableWidget_ListEmp.insertRow(row)

            item_id = QTableWidgetItem(str(employee.ID))
            self.tableWidget_ListEmp.setItem(row, 0, item_id)

            if employee.IsDeleted == 1:
                item_id.setBackground(Qt.GlobalColor.red)

            item_code = QTableWidgetItem(str(employee.EmployeeCode))
            self.tableWidget_ListEmp.setItem(row, 1, item_code)

            item_name = QTableWidgetItem(str(employee.Name))
            self.tableWidget_ListEmp.setItem(row, 2, item_name)

            item_phone = QTableWidgetItem(str(employee.Phone))
            self.tableWidget_ListEmp.setItem(row, 3, item_phone)

            item_email = QTableWidgetItem(str(employee.Email))
            self.tableWidget_ListEmp.setItem(row, 4, item_email)

    def setupSignalAndSlot(self):
        self.pushButton_New.clicked.connect(self.clearAll)
        self.tableWidget_ListEmp.itemSelectionChanged.connect(self.showDetailEmployee)
        self.pushButton_Save.clicked.connect(self.saveEmployee)
        self.pushButton_Update.clicked.connect(self.updateEmployee)

    def updateEmployee(self):
        self.is_completed = False
        id = self.lineEdit_EmpID.text()
        code = self.lineEdit_EmpCode.text()
        name = self.lineEdit_EmpName.text()
        phone = self.lineEdit_EmpPhone.text()
        email = self.lineEdit_Email.text()
        password = self.lineEdit_EmpPassword.text()
        is_deleted = self.checkBox_IsDeleted.isChecked()
        print(int(is_deleted))
        emp = Employee(id, code, name, phone, email, password, int(is_deleted))
        print(emp)
        result = self.empc.updateOneEmployee(emp)
        if result > 0:
            self.displayEmployeeIntoTable()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Success to update employee")
            msg.setWindowTitle("Update Successfully")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Failed to update new employee")
            msg.setWindowTitle("Update Falied")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed = True

    def clearAll(self):
        self.lineEdit_EmpID.clear()
        self.lineEdit_EmpName.clear()
        self.lineEdit_EmpPhone.clear()
        self.lineEdit_Email.clear()
        self.lineEdit_EmpCode.clear()
        self.lineEdit_EmpPassword.clear()

        self.lineEdit_EmpID.setFocus()

    def showDetailEmployee(self):
        row_index = self.tableWidget_ListEmp.currentRow() # Trả về dòng
        print("You clicked at: ", row_index) # nếu dùng currentIndex --> row_index.row()
        id = self.tableWidget_ListEmp.item(row_index, 0).text()
        print(id)
        emp = self.empc.getDetailEmployee(id)
        print(emp)
        print('Kiểu dữ liệu: ',type(emp.IsDeleted))
        if emp:
            self.lineEdit_EmpID.setText(str(emp.ID))
            self.lineEdit_EmpCode.setText(str(emp.EmployeeCode))
            self.lineEdit_EmpName.setText(str(emp.Name))
            self.lineEdit_EmpPhone.setText(str(emp.Phone))
            self.lineEdit_Email.setText(str(emp.Email))
            if emp.IsDeleted == 1:
                self.checkBox_IsDeleted.setChecked(True)
                print("Checked chưa?", self.checkBox_IsDeleted.isChecked())
            else:
                self.checkBox_IsDeleted.setChecked(False)
    def saveEmployee(self):
        self.is_completed = False
        code = self.lineEdit_EmpCode.text()
        name = self.lineEdit_EmpName.text()
        phone = self.lineEdit_EmpPhone.text()
        email = self.lineEdit_Email.text()
        password = self.lineEdit_EmpPassword.text()
        emp = Employee(None, code, name, phone, email, password, 0)
        result = self.empc.insertOneEmployee(emp)
        if result > 0:
            self.displayEmployeeIntoTable()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Failed to insert new employee")
            msg.setWindowTitle("Insert Falied")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed = True

    def deleteEmployee(self):
        self.is_completed = False
        id = self.lineEdit_EmpID.text()
        result = self.empc.deleteOneEmployee(id)
        if result > 0:
            self.displayEmployeeIntoTable()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Failed to delete employee")
            msg.setWindowTitle("Delete Falied")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed = True





