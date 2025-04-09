import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QGraphicsView, QTextEdit, QPushButton, \
    QMessageBox
from Loader import Loader
from ZoomableGraphicsView import ZoomableGraphicsView
from src.Tester import Tester


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setGeometry(85, 300, 1750, 640)
        self.setWindowTitle("OCR Application")

        self.main_win = uic.loadUi("main_win.ui")
        self.image_win = uic.loadUi("image_menu.ui")
        self.dataset_win = uic.loadUi("dataset_menu.ui")

        self.central_widget.addWidget(self.main_win)
        self.central_widget.addWidget(self.image_win)
        self.central_widget.addWidget(self.dataset_win)

        self.main_win.image_button.clicked.connect(self.show_ocr_menu)
        self.main_win.dataset_button.clicked.connect(self.show_testing_menu)
        self.image_win.back_btn.clicked.connect(self.show_main_menu)
        self.dataset_win.back_btn.clicked.connect(self.show_main_menu)

        dataset_image_view = self.dataset_win.findChild(ZoomableGraphicsView, "image_view")
        self.loader_dataset_img = Loader(dataset_image_view, "Image")
        self.dataset_win.upload_img_btn.clicked.connect(self.loader_dataset_img.load_image)

        dataset_annotation_view = self.dataset_win.findChild(QGraphicsView, "annotation_view")
        self.loader_dataset_ann = Loader(dataset_annotation_view, "Annotation")
        self.dataset_win.upload_ann_btn.clicked.connect(self.loader_dataset_ann.load_text)

        dataset_results_view = self.dataset_win.findChild(QGraphicsView, "results_view")
        self.loader_dataset_res = Loader(dataset_results_view, "Results")

        dataset_stats_view = self.dataset_win.findChild(QGraphicsView, "stats_view")
        self.loader_dataset_stats = Loader(dataset_stats_view, "Statistics")

        image_image_view = self.image_win.findChild(ZoomableGraphicsView, "image_view")
        self.loader_image_img = Loader(image_image_view, "Image")
        self.image_win.open_img_btn.clicked.connect(self.loader_image_img.load_image)

        image_annotation_view = self.image_win.findChild(QGraphicsView, "annotation_view")
        self.loader_image_ann = Loader(image_annotation_view, "Annotation")
        self.image_win.upload_ann_btn.clicked.connect(self.loader_image_ann.load_text)

        image_results_view = self.image_win.findChild(QGraphicsView, "results_view")
        self.loader_image_res = Loader(image_results_view, "Results")

        image_stats_view = self.image_win.findChild(QGraphicsView, "stats_view")
        self.loader_image_stats = Loader(image_stats_view, "Statistics")

        self.central_widget.setCurrentWidget(self.main_win)
        self.show()

        self.image_win.test_btn = self.image_win.findChild(QPushButton, "test_btn")
        self.image_win.test_btn.clicked.connect(self.perform_test)

        self.dataset_win.test_btn = self.dataset_win.findChild(QPushButton, "test_btn")
        #self.dataset_win.test_btn.clicked.connect(self.perform_test, self.loader_dataset_img, self.loader_dataset_ann)

    def show_main_menu(self):
        self.central_widget.setCurrentWidget(self.main_win)

    def show_ocr_menu(self):
        self.central_widget.setCurrentWidget(self.image_win)

    def show_testing_menu(self):
        self.central_widget.setCurrentWidget(self.dataset_win)

    def perform_test(self):
        try:
            image_path = self.loader_image_img.get_image()
            annotation = self.loader_image_ann.get_annotation()
            if not image_path:
                print("Image path is missing. Please load an image.")
                return
            if not annotation:
                print("Annotation is missing. Please load an annotation file.")
                return
            tester = Tester()
            metrics, ocr_results = tester.test_ocr(image_path, annotation)
            metricss = {
                system: {
                    "CER": metrics[system].get("CER", "N/A"),
                    "WER": metrics[system].get("WER", "N/A")
                }
                for system in ocr_results.keys()
            }
            self.loader_image_stats.display_metrics(metricss)
            self.loader_image_res.display_results(ocr_results)

        except Exception as e:
            print(f"An error occurred during the test: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()