from PyQt5 import uic
from PyQt5.QtWidgets import *

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setGeometry(300, 300, 1080, 640)
        self.setWindowTitle("OCR Application")

        self.main_win = uic.loadUi("main_win.ui")
        self.ocr_win = uic.loadUi("ocr_menu.ui")
        self.test_win = uic.loadUi("testing_menu.ui")

        self.central_widget.addWidget(self.main_win)
        self.central_widget.addWidget(self.ocr_win)
        self.central_widget.addWidget(self.test_win)

        self.main_win.ocr_sys_button.clicked.connect(self.show_ocr_menu)
        self.main_win.testing_button.clicked.connect(self.show_testing_menu)
        self.ocr_win.back_btn.clicked.connect(self.show_main_menu)
        self.test_win.back_btn.clicked.connect(self.show_main_menu)

        self.central_widget.setCurrentWidget(self.main_win)
        self.show()

    def show_main_menu(self):
        self.central_widget.setCurrentWidget(self.main_win)

    def show_ocr_menu(self):
        self.central_widget.setCurrentWidget(self.ocr_win)

    def show_testing_menu(self):
        self.central_widget.setCurrentWidget(self.test_win)

if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()