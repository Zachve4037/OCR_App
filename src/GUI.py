import traceback
from src.OCRSystems import OCRSystem
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QGraphicsView, QTextEdit, QPushButton, \
    QMessageBox, QFileDialog, QRadioButton
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

        self.image_win.tesseract_btn = self.image_win.findChild(QRadioButton, "tesseract_btn")
        self.image_win.easyocr_btn = self.image_win.findChild(QRadioButton, "easyocr_btn")
        self.image_win.ocrmypdf_btn = self.image_win.findChild(QRadioButton, "ocrmypdf_btn")

        dataset_image_view = self.dataset_win.findChild(QGraphicsView, "image_view")
        self.loader_dataset_img = Loader(dataset_image_view, "Image")
        self.dataset_win.upload_img_btn.clicked.connect(self.loader_dataset_img.open_image_folder)

        dataset_annotation_view = self.dataset_win.findChild(QGraphicsView, "annotation_view")
        self.loader_dataset_ann = Loader(dataset_annotation_view, "Annotation")
        self.dataset_win.upload_ann_btn.clicked.connect(self.loader_dataset_ann.open_annotation_folder)

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
        self.dataset_win.test_btn.clicked.connect(self.perform_dataset_test)

        self.dataset_win.export_btn = self.dataset_win.findChild(QPushButton, "export_btn")
        self.dataset_win.export_btn.clicked.connect(self.export_metrics)

        self.dataset_win.export_results_btn = self.dataset_win.findChild(QPushButton, "export_results_btn")
        self.dataset_win.export_results_btn.clicked.connect(self.export_results)

        self.image_win.export_results_btn = self.image_win.findChild(QPushButton, "export_results_btn")
        self.image_win.export_results_btn.clicked.connect(self.export_image_results)

    def export_image_results(self):
            try:
                self.loader_image_res.export_image_results(self.image_ocr_results)
            except AttributeError:
                print("No results available to export. Please run the test first.")

    def export_results(self):
        try:
            self.loader_dataset_res.export_results(self.all_ocr_results)
        except AttributeError:
            print("No results available to export. Please run the dataset test first.")

    def export_metrics(self):
        self.loader_dataset_stats.export_metrics()

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
                selected_system = None
                if self.image_win.tesseract_btn.isChecked():
                    selected_system = "Tesseract"
                elif self.image_win.easyocr_btn.isChecked():
                    selected_system = "EasyOCR"
                elif self.image_win.ocrmypdf_btn.isChecked():
                    selected_system = "OCRmyPDF"

                if selected_system:
                    tester = Tester()
                    ocr_system = OCRSystem()
                    ocr_result = None

                    if selected_system == "Tesseract":
                        ocr_result = ocr_system.ocr_tesseract(image_path)
                    elif selected_system == "EasyOCR":
                        ocr_result = ocr_system.ocr_easyocr(image_path)
                    elif selected_system == "OCRmyPDF":
                        ocr_result = ocr_system.ocr_ocrmypdf(image_path)

                    if ocr_result:
                        self.loader_image_res.display_results_img({selected_system: ocr_result}, None)
                        self.image_ocr_results = {selected_system: ocr_result}
                    else:
                        print(f"OCR failed for {selected_system}.")
                else:
                    print("No OCR system selected. Please select a system.")
            else:
                tester = Tester()
                metrics, ocr_results = tester.test_ocr(image_path, annotation)
                metricss = {
                    system: {
                        "CER": metrics[system].get("CER", "N/A"),
                        "WER": metrics[system].get("WER", "N/A")
                    }
                    for system in ocr_results.keys()
                }

                self.loader_image_stats.display_metrics_img(metricss)
                self.loader_image_res.display_results_img(ocr_results, annotation)
                self.image_ocr_results = ocr_results
        except Exception as e:
            print(f"An error occurred during the test: {e}")
            traceback.print_exc()

    def perform_dataset_test(self):
        try:
            image_folder = self.loader_dataset_img.get_image_folder()
            annotation_folder = self.loader_dataset_ann.get_annotation_folder()
            if not image_folder or not annotation_folder:
                print("Both image and annotation folders must be selected.")
                return
            tester = Tester()
            all_metrics = {}
            all_ocr_results = {}
            all_annotations = {}
            for image_file in os.listdir(image_folder):
                image_path = os.path.join(image_folder, image_file)
                annotation_path = os.path.join(annotation_folder, os.path.splitext(image_file)[0] + ".txt")
                if not os.path.exists(annotation_path):
                    print(f"Annotation file for {image_file} not found. Skipping...")
                    continue
                with open(annotation_path, 'r') as file:
                    annotation = file.read()
                all_annotations[image_file] = annotation
                metrics, ocr_results = tester.test_ocr(image_path, annotation)
                all_metrics[image_file] = metrics
                all_ocr_results[image_file] = ocr_results
            self.all_ocr_results = all_ocr_results
            self.loader_dataset_stats.display_metrics_dtst(all_metrics)
            self.loader_dataset_res.display_results_dtst(all_ocr_results, all_annotations)
        except Exception as e:
            print(f"An error occurred during the dataset test: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()