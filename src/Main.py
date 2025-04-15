import sys
from PyQt5.QtWidgets import QApplication
import GUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI.GUI()
    sys.exit(app.exec_())