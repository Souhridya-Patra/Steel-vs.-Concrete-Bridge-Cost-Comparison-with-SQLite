import sys
import tkinter as tk
from PyQt5.QtWidgets import QApplication
from gui import BridgeCostApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BridgeCostApp()
    window.show()
    root = tk.Tk()
    root.withdraw()
    sys.exit(app.exec_())