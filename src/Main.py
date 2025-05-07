import sys

from PyQt5.QtWidgets import QApplication

import GUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI.GUI()
    sys.exit(app.exec_())

# nuitka --standalone --onefile --include-data-file=.venv/Lib/site-packages/ocrmypdf/data/pdf.ttf=ocrmypdf/data/pdf.ttf --module-parameter=torch-disable-jit=yes --enable-plugin=pyqt5 src/Main.py