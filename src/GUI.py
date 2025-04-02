from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QGraphicsView, QTextEdit, QPushButton
from Loader import Loader
from ZoomableGraphicsView import ZoomableGraphicsView
from src.Tester import Tester


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

        test_ocr_view = self.test_win.findChild(ZoomableGraphicsView, "image_view")
        self.loader_test_img = Loader(test_ocr_view, "Image")
        self.test_win.upload_btn.clicked.connect(self.loader_test_img.load_image)

        test_text_view = self.test_win.findChild(QGraphicsView, "annotation_view")
        self.loader_test_text = Loader(test_text_view, "Annotation")
        self.test_win.annotation_btn.clicked.connect(self.loader_test_text.load_text)

        ocr_img_view = self.ocr_win.findChild(ZoomableGraphicsView, "image_view")
        self.loader_ocr_img = Loader(ocr_img_view, "Image")
        self.ocr_win.upload_btn.clicked.connect(self.loader_ocr_img.load_image)

        self.central_widget.setCurrentWidget(self.main_win)
        self.show()

        self.test_win.test_btn = self.test_win.findChild(QPushButton, "test_btn")
        self.test_win.test_btn.clicked.connect(self.perform_test)

    def show_main_menu(self):
        self.central_widget.setCurrentWidget(self.main_win)

    def show_ocr_menu(self):
        self.central_widget.setCurrentWidget(self.ocr_win)

    def show_testing_menu(self):
        self.central_widget.setCurrentWidget(self.test_win)

    def perform_test(self):
        try:
            image_path = self.loader_test_img.get_image()
            annotation = self.loader_test_text.get_annotation()

            if not image_path:
                print("Image path is missing. Please load an image.")
                return
            if not annotation:
                print("Annotation is missing. Please load an annotation file.")
                return

            tester = Tester()
            metrics = tester.test_ocr(image_path, annotation)

            for system, metric in metrics.items():
                print(f"{system} Metrics: {metric} \n")

        except Exception as e:
            print(f"An error occurred during the test: {e}")

if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()