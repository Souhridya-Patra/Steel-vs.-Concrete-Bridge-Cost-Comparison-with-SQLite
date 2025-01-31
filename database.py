import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QFormLayout, QMessageBox
)

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Input Window")
        self.setGeometry(200, 200, 600, 500)

        self.conn = sqlite3.connect("bridge_costs.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.fields = [
            "Steel Base Rate(INR/m^2)",
            "Steel Maintenance Rate(INR/m^2/year)",
            "Steel Repair Rate(INR/m^2)",
            "Steel Demolition Rate(INR/m^2)",
            "Steel Environmental Factor(INR/m^2)",
            "Steel Social Factor(INR/vehicle/year)",
            "Steel Delay Factor(INR/vehicle/year)",
            "Concrete Base Rate(INR/m^2)",
            "Concrete Maintenance Rate(INR/m^2/year)",
            "Concrete Repair Rate(INR/m^2)",
            "Concrete Demolition Rate(INR/m^2)",
            "Concrete Environmental Factor(INR/m^2)",
            "Concrete Social Factor(INR/vehicle/year)",
            "Concrete Delay Factor(INR/vehicle/year)",
        ]

        self.inputs = {}
        form_layout = QFormLayout()

        for field in self.fields:
            input_field = QLineEdit(self)
            self.inputs[field] = input_field
            form_layout.addRow(QLabel(field), input_field)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.update_database)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.confirm_data)

        form_layout.addWidget(self.submit_button)
        form_layout.addWidget(self.confirm_button)
        self.setLayout(form_layout)

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            steel_base_rate REAL,
            steel_maintenance_rate REAL,
            steel_repair_rate REAL,
            steel_demolition_rate REAL,
            steel_environmental_factor REAL,
            steel_social_factor REAL,
            steel_delay_factor REAL,
            concrete_base_rate REAL,
            concrete_maintenance_rate REAL,
            concrete_repair_rate REAL,
            concrete_demolition_rate REAL,
            concrete_environmental_factor REAL,
            concrete_social_factor REAL,
            concrete_delay_factor REAL
        )
        """)
        self.conn.commit()

    def update_database(self):
        try:
            self.values = [float(self.inputs[field].text()) for field in self.fields]
            self.confirm_button.setEnabled(True)
            QMessageBox.information(self, "Step 1: Submitted", "Data submitted. Click 'Confirm' to finalize.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def confirm_data(self):
        try:
            self.cursor.execute("DELETE FROM rates")
            self.cursor.execute("""
            INSERT INTO rates (
                steel_base_rate, steel_maintenance_rate, steel_repair_rate, steel_demolition_rate,
                steel_environmental_factor, steel_social_factor, steel_delay_factor,
                concrete_base_rate, concrete_maintenance_rate, concrete_repair_rate, concrete_demolition_rate,
                concrete_environmental_factor, concrete_social_factor, concrete_delay_factor
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, self.values)
            self.conn.commit()

            QMessageBox.information(self, "Success", "Data has been finalized.")
            self.confirm_button.setEnabled(False)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()