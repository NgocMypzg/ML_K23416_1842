import sys
import os
import datetime
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog,
    QTableWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox,
    QTableWidgetItem, QComboBox
)
from PyQt6.QtCore import Qt

from FileUtil import FileUtil


class HousePriceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("House Pricing Prediction - PyQt6")
        self.resize(1200, 800)
        self.df = None
        self.lm = None
        self.data_dir = "../../Data"

        # --- Widgets ---
        self.file_input = QLineEdit("Data/USA_Housing.csv")
        self.btn_browse = QPushButton("1. Pick Dataset")
        self.btn_view = QPushButton("2. View Dataset")

        # training rate input
        self.train_rate_input = QLineEdit("80")

        self.btn_train = QPushButton("3. Train Model")
        self.btn_eval = QPushButton("4. Evaluate Model")
        self.btn_save = QPushButton("5. Save Model")
        self.btn_load = QPushButton("6. Load Model")
        self.btn_predict = QPushButton("7. Predict")

        self.model_dropdown = QComboBox()
        self.update_model_dropdown()

        self.input_income = QLineEdit()
        self.input_age = QLineEdit()
        self.input_rooms = QLineEdit()
        self.input_bedrooms = QLineEdit()
        self.input_pop = QLineEdit()
        self.input_price = QLineEdit()
        self.input_price.setReadOnly(True)

        self.mae_label = QLabel("MAE: ")
        self.mse_label = QLabel("MSE: ")
        self.rmse_label = QLabel("RMSE: ")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Avg. Area Income", "Avg. Area House Age", "Avg. Area Number of Rooms",
            "Avg. Area Number of Bedrooms", "Area Population", "Actual Price", "Predicted Price"
        ])

        # Layout
        main_layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Select Dataset:"))
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.btn_browse)
        file_layout.addWidget(self.btn_view)

        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("Training Rate (%):"))
        action_layout.addWidget(self.train_rate_input)
        action_layout.addSpacing(20)
        action_layout.addWidget(self.btn_train)
        action_layout.addWidget(self.btn_eval)
        action_layout.addWidget(self.btn_save)
        action_layout.addSpacing(20)
        action_layout.addWidget(QLabel("Select Model:"))
        action_layout.addWidget(self.model_dropdown)
        action_layout.addWidget(self.btn_load)

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Avg. Area Income:"), 0, 0)
        form_layout.addWidget(self.input_income, 0, 1)
        form_layout.addWidget(QLabel("Avg. Area House Age:"), 1, 0)
        form_layout.addWidget(self.input_age, 1, 1)
        form_layout.addWidget(QLabel("Avg. Area Number of Rooms:"), 2, 0)
        form_layout.addWidget(self.input_rooms, 2, 1)
        form_layout.addWidget(QLabel("Avg. Area Number of Bedrooms:"), 3, 0)
        form_layout.addWidget(self.input_bedrooms, 3, 1)
        form_layout.addWidget(QLabel("Area Population:"), 4, 0)
        form_layout.addWidget(self.input_pop, 4, 1)
        form_layout.addWidget(self.btn_predict, 5,1)
        form_layout.addWidget(QLabel("Predicted Price:"), 6, 0)
        form_layout.addWidget(self.input_price, 6, 1)

        metrics_layout = QHBoxLayout()
        metrics_layout.addWidget(self.mae_label)
        metrics_layout.addWidget(self.mse_label)
        metrics_layout.addWidget(self.rmse_label)

        main_layout.addLayout(file_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(metrics_layout)
        self.setLayout(main_layout)

        # Signals
        self.btn_browse.clicked.connect(self.do_pick_data)
        self.btn_view.clicked.connect(self.do_view_dataset)
        self.btn_train.clicked.connect(self.do_train)
        self.btn_eval.clicked.connect(self.do_evaluate)
        self.btn_save.clicked.connect(self.do_save_model)
        self.btn_load.clicked.connect(self.do_load_model)


    # --- Functionalities ---
    def do_pick_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Dataset", "", "CSV Files (*.csv)")
        if file_name:
            self.file_input.setText(file_name)

    def do_view_dataset(self):
        file_path = self.file_input.text()
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Warning", "Dataset not found!")
            return
        df = pd.read_csv(file_path)
        self.table.setRowCount(0)
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for r in range(min(500, len(df))):
            row = df.iloc[r].values
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def do_train(self):
        try:
            df = pd.read_csv(self.file_input.text())
        except Exception:
            QMessageBox.critical(self, "Error", "Không đọc được dataset!")
            return

        try:
            rate = float(self.train_rate_input.text()) / 100
            if rate <= 0 or rate >= 1:
                raise ValueError
        except Exception:
            QMessageBox.warning(self, "Warning", "Vui lòng nhập phần trăm train hợp lệ (1-99)!")
            return

        X = df[['Avg. Area Income', 'Avg. Area House Age',
                'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms',
                'Area Population']]
        y = df['Price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - rate, random_state=101)
        self.lm = LinearRegression()
        self.lm.fit(X_train, y_train)
        self.X_test, self.y_test = X_test, y_test

        QMessageBox.information(self, "Info", f"Đã train mô hình với {rate*100:.0f}% dữ liệu!")

    def do_evaluate(self):
        if self.lm is None:
            QMessageBox.warning(self, "Warning", "Chưa có model để đánh giá!")
            return

        preds = self.lm.predict(self.X_test)
        mae = metrics.mean_absolute_error(self.y_test, preds)
        mse = metrics.mean_squared_error(self.y_test, preds)
        rmse = np.sqrt(mse)

        self.mae_label.setText(f"MAE: {mae:.2f}")
        self.mse_label.setText(f"MSE: {mse:.2f}")
        self.rmse_label.setText(f"RMSE: {rmse:.2f}")

        self.table.setRowCount(0)
        for i in range(len(self.X_test)):
            row_vals = list(self.X_test.iloc[i]) + [self.y_test.iloc[i], preds[i]]
            self.table.insertRow(i)
            for j, val in enumerate(row_vals):
                self.table.setItem(i, j, QTableWidgetItem(str(round(val, 2))))

        QMessageBox.information(self, "Info", "Đánh giá hoàn tất!")

    def do_save_model(self):
        if self.lm is None:
            QMessageBox.warning(self, "Warning", "Chưa có model để lưu!")
            return

        reply = QMessageBox.question(self, "Save Model",
                                     "Bạn có chắc chắn muốn lưu mô hình này không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        os.makedirs(self.data_dir, exist_ok=True)
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.data_dir, f"housingmodel_{now}.zip")

        if FileUtil.savemodel(self.lm, filename):
            QMessageBox.information(self, "Info", f"Đã lưu mô hình: {filename}")
            self.update_model_dropdown()
        else:
            QMessageBox.critical(self, "Error", "Lưu mô hình thất bại!")

    def do_load_model(self):
        model_name = self.model_dropdown.currentText()
        if not model_name or model_name == "No models":
            QMessageBox.warning(self, "Warning", "Không có model để nạp!")
            return

        model_path = os.path.join(self.data_dir, model_name)
        self.lm = FileUtil.loadmodel(model_path)
        if self.lm:
            QMessageBox.information(self, "Info", f"Đã nạp mô hình: {model_name}")
        else:
            QMessageBox.critical(self, "Error", "Nạp mô hình thất bại!")

    def do_predict(self):
        if self.lm is None:
            QMessageBox.warning(self, "Warning", "Chưa có model để dự đoán!")
            return
        try:
            vals = [float(self.input_income.text()),
                    float(self.input_age.text()),
                    float(self.input_rooms.text()),
                    float(self.input_bedrooms.text()),
                    float(self.input_pop.text())]
            result = self.lm.predict([vals])
            self.input_price.setText(str(round(result[0], 2)))
        except Exception:
            QMessageBox.critical(self, "Error", "Vui lòng nhập đúng định dạng số!")

    def get_model_files(self):
        os.makedirs(self.data_dir, exist_ok=True)
        files = [f for f in os.listdir(self.data_dir) if f.endswith(".zip")]
        return files if files else ["No models"]

    def update_model_dropdown(self):
        self.model_dropdown.clear()
        self.model_dropdown.addItems(self.get_model_files())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HousePriceApp()
    window.show()
    sys.exit(app.exec())
