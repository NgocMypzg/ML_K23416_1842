from PyQt6.QtWidgets import QMessageBox

from RetailProject.Connectors.Employee_Connector import Employee_Connector
from RetailProject.UI.MainWindow import Ui_MainWindow


class LoginWindowEx(Ui_MainWindow):
    def __init__(self):
        pass
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.showWindow()
        self.setupSignalandSlots()

    def showWindow(self):
        self.MainWindow.show()
    def setupSignalandSlots(self):
        self.pushButtonLogin.clicked.connect(self.processLogin)
    def processLogin(self):
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()
        empc = Employee_Connector()
        emp = empc.login(email, password)
        if emp is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Employee Connector Login Failed")
            msg.setWindowTitle("Login Falied")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Employee Connector Login Successful")
            msg.setWindowTitle("Login Successful")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()