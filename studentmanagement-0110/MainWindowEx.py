import base64
import traceback
import mysql.connector
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from MainWindow import Ui_MainWindow
# import pymysql
class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.default_avatar="images/default.jpg"
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None
        self.intro = None
        self.conn = self.connectMySQL()
        # self.selectAllStudent()

    def processItemSelection(self):
        row = self.tableWidget_students.currentRow()
        if row == -1:
            return
        try:
            code = self.tableWidget_students.item(row, 1).text()
            cursor = self.conn.cursor()
            # query all students
            sql = "select * from student where code=%s"
            val = (code,)
            cursor.execute(sql, val)
            item = cursor.fetchone()
            if item != None:
                self.id = item[0]
                self.code = item[1]
                self.name = item[2]
                self.age = item[3]
                self.avatar = item[4]
                self.intro = item[5]
                self.lineEdit_id.setText(str(self.id))
                self.lineEdit_code.setText(self.code)
                self.lineEdit_name.setText(self.name)
                self.lineEdit_age.setText(str(self.age))
                self.lineEdit_intro.setText(self.intro)
                # self.labelAvatar.setPixmap(None)
                if self.avatar != None:
                    imgdata = base64.b64decode(self.avatar)
                    pixmap = QPixmap()
                    pixmap.loadFromData(imgdata)
                    self.label_image.setPixmap(pixmap)
                else:
                    pixmap = QPixmap("images/ic_no_avatar.png")

                    self.label_image.setPixmap(pixmap)
            else:
                print("Not Found")
            cursor.close()
        except:
            traceback.print_exc()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.tableWidget_students.itemSelectionChanged.connect(self.processItemSelection)
        self.pushButton_avatar.clicked.connect(self.pickAvatar)
        self.pushButton_removeavatar.clicked.connect(self.removeAvatar)
        self.pushButton_insert.clicked.connect(self.processInsert)
        self.pushButton_update.clicked.connect(self.processUpdate)
        self.pushButton_remove.clicked.connect(self.processRemove)

    def connectMySQL(self):

        config = {
            'host': "localhost",
            'port': 3306,
            'database': "studentmanagement",
            'user': "root",
            'password': "3141592653589793Mk."
        }
        conn = mysql.connector.connect(**config)
        return conn

    def pickAvatar(self):
        filters = "Picture PNG (*.png);;All files(*)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self.MainWindow,
            filter=filters,
        )
        if filename == '':
            return
        pixmap = QPixmap(filename)
        self.label_image.setPixmap(pixmap)

        with open(filename, "rb") as image_file:
            self.avatar = base64.b64encode(image_file.read())
            print(self.avatar)
        pass

    def processInsert(self):
        try:
            cursor = self.conn.cursor()
            # query all students
            sql = "insert into student(Code,Name,Age,Avatar,Intro) values(%s,%s,%s,%s,%s)"

            self.code = self.lineEdit_code.text()
            self.name = self.lineEdit_name.text()
            self.age = int(self.lineEdit_age.text())
            if not hasattr(self, 'avatar'):
                avatar = None
            intro = self.lineEdit_intro.text()
            val = (self.code, self.name, self.age, self.avatar, self.intro)

            cursor.execute(sql, val)

            self.conn.commit()

            print(cursor.rowcount, " record inserted")
            self.lineEdit_id.setText(str(cursor.lastrowid))

            cursor.close()
            self.selectAllStudent()
        except:
            traceback.print_exc()

    def selectAllStudent(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "select * from student"
        cursor.execute(sql)
        dataset = cursor.fetchall()
        self.tableWidget_students.setRowCount(0)
        row = 0
        for item in dataset:
            row = self.tableWidget_students.rowCount()
            self.tableWidget_students.insertRow(row)

            self.id = item[0]
            self.code = item[1]
            self.name = item[2]
            self.age = item[3]
            self.avatar = item[4]
            self.intro = item[5]

            self.tableWidget_students.setItem(row, 0, QTableWidgetItem(str(self.id)))
            self.tableWidget_students.setItem(row, 1, QTableWidgetItem(self.code))
            self.tableWidget_students.setItem(row, 2, QTableWidgetItem(self.name))
            self.tableWidget_students.setItem(row, 3, QTableWidgetItem(str(self.age)))

        cursor.close()
    def removeAvatar(self):
        self.avatar = None
        pixmap = QPixmap(self.default_avatar)
        self.label_image.setPixmap(pixmap)

    def processUpdate(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "update student set Code=%s,Name=%s,Age=%s,Avatar=%s,Intro=%s" \
              " where Id=%s"
        self.id = int(self.lineEdit_id.text())
        self.code = self.lineEdit_code.text()
        self.name = self.lineEdit_name.text()
        self.age = int(self.lineEdit_age.text())
        if not hasattr(self, 'avatar'):
            self.avatar = None
        self.intro = self.lineEdit_intro.text()

        val = (self.code, self.name, self.age, self.avatar, self.intro, self.id)

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record updated")
        cursor.close()
        self.selectAllStudent()

    def processRemove(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.No:
            return
        cursor = self.conn.cursor()
        # query all students
        sql = "delete from student " \
              " where Id=%s"

        val = (self.lineEdit_id.text(),)

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record removed")

        cursor.close()
        self.selectAllStudent()
        self.clearData()

    def clearData(self):
        self.lineEdit_id.setText("")
        self.lineEdit_code.setText("")
        self.lineEdit_name.setText("")
        self.lineEdit_age.setText("")
        self.lineEdit_intro.setText("")
        self.avatar = None
    def show(self):
        self.MainWindow.show()