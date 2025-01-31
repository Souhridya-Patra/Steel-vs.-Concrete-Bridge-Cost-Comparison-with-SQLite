from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QSpacerItem,
    QSizePolicy, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from calculations import calculate_costs
from plot import plot_costs
from database import InputWindow
import tkinter as tk
from tkinter import filedialog


class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Comparison")
        self.setGeometry(100, 100, 1580, 920)
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        #left panel
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Span Length (m):"))
        self.span_input = QLineEdit()
        input_layout.addWidget(self.span_input)
        input_layout.addSpacing(20)

        input_layout.addWidget(QLabel("Width (m):"))
        self.width_input = QLineEdit()
        input_layout.addWidget(self.width_input)
        input_layout.addSpacing(20)

        input_layout.addWidget(QLabel("Traffic Volume (vehicles/day):"))
        self.traffic_input = QLineEdit()
        input_layout.addWidget(self.traffic_input)
        input_layout.addSpacing(20)

        input_layout.addWidget(QLabel("Design Life (years):"))
        self.design_input = QLineEdit()
        input_layout.addWidget(self.design_input)
        input_layout.addSpacing(300)

        self.calculate_button = QPushButton("Calculate Costs")
        self.calculate_button.clicked.connect(self.calculate_costs)
        input_layout.addWidget(self.calculate_button)

        self.update_db_button = QPushButton("Update Database")
        self.update_db_button.clicked.connect(self.open_new_window)
        input_layout.addWidget(self.update_db_button)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        #center panel
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.canvas)
        center_widget = QWidget()
        center_widget.setLayout(center_layout)

        #right panel
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Calculated Costs:"))
        self.cost_table = QTableWidget()
        self.cost_table.setRowCount(8)
        self.cost_table.setColumnCount(3)
        self.cost_table.setHorizontalHeaderLabels(["Cost Component", "Steel(₹)", "Concrete(₹)"])
        output_layout.addWidget(self.cost_table)

        self.export_plot_button = QPushButton("Export Plot")
        self.export_plot_button.clicked.connect(self.export_plot)
        output_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        output_layout.addWidget(self.export_plot_button)

        output_widget = QWidget()
        output_widget.setLayout(output_layout)

        #main layout
        main_layout.addWidget(input_widget, 1)
        main_layout.addWidget(center_widget, 4)
        main_layout.addWidget(output_widget, 2)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def calculate_costs(self):
        try:
            span_length = float(self.span_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_input.text())
            design_life = float(self.design_input.text())

            steel_costs, concrete_costs = calculate_costs(span_length, width, traffic_volume, design_life)

            #plot
            self.figure = plot_costs(steel_costs, concrete_costs)
            self.canvas.figure = self.figure
            self.canvas.draw()

            #cost table
            self.cost_table.setColumnWidth(0, 170)
            self.cost_table.setColumnWidth(1, 120)
            self.cost_table.setColumnWidth(2, 120)
            cost_labels = ["Construction Cost", "Maintenance Cost", "Repair Cost", "Demolition Cost", "Environmental Cost", "Social Cost", "User Cost", "Total Cost"]

            for k in range(8):
                self.cost_table.setItem(k, 0, QTableWidgetItem(cost_labels[k]))
                self.cost_table.setItem(k, 1, QTableWidgetItem(f"{steel_costs[cost_labels[k]]:.2f}"))
                self.cost_table.setItem(k, 2, QTableWidgetItem(f"{concrete_costs[cost_labels[k]]:.2f}"))

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values.")
        except IndexError:
            QMessageBox.warning(self, "Error", "The database is empty. Please update the database first.")

    def open_new_window(self):
        self.new_window = InputWindow()
        self.new_window.show()

    def export_plot(self):
        directory = filedialog.asksaveasfilename(title='Asking File Name')
        file_name = directory + '.png'
        self.figure.savefig(file_name, dpi=300)