import csv
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsTextItem, QTableWidgetItem, QTableWidget


class Loader:
    def __init__(self, view, text):
        self.view = view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.add_background_text(text)
        self.annotation = ""
        self.image = None
        self.image_folder = None
        self.annotation_folder = None
        self.table_widget = None

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if file_name:
            self.image = file_name
            pixmap = QPixmap(file_name)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.view.fitInView(self.scene.itemsBoundingRect(), mode=1)

    def load_text(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Annotation File", "", "Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.annotation = file.read()
                self.scene.clear()
                self.add_annotation_text(self.annotation)

    def open_image_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Image Folder")
        if folder:
            self.image_folder = folder
            print(f"Selected Image Folder: {self.image_folder}")
            self.scene.clear()
            for file_name in os.listdir(folder):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    text_item = QGraphicsTextItem(file_name)
                    font = QFont("Arial", 10)
                    text_item.setFont(font)
                    text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
                    self.scene.addItem(text_item)
                    text_item.setPos(10, 10 + len(self.scene.items()) * 20)

    def open_annotation_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Annotation Folder")
        if folder:
            self.annotation_folder = folder
            print(f"Selected Annotation Folder: {self.annotation_folder}")
            self.scene.clear()
            for file_name in os.listdir(folder):
                if file_name.lower().endswith('.txt'):
                    text_item = QGraphicsTextItem(file_name)
                    font = QFont("Arial", 10)
                    text_item.setFont(font)
                    text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
                    self.scene.addItem(text_item)
                    text_item.setPos(10, 10 + len(self.scene.items()) * 20)

    def display_metrics_dtst(self, metrics, times):
        self.scene.clear()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Image Name", "System", "CER", "WER", "Time (s)"])
        self.table_widget.setSortingEnabled(True)

        row = 0
        system_averages = {}

        for image_name, systems_metrics in metrics.items():
            for system, metric in systems_metrics.items():
                cer = f"{metric.get('CER'):.2f}" if isinstance(metric.get("CER"), (int, float)) else "N/A"
                wer = f"{metric.get('WER'):.2f}" if isinstance(metric.get("WER"), (int, float)) else "N/A"
                time_taken = f"{times[image_name].get(system, 0):.2f}"

                self.table_widget.insertRow(row)
                self.table_widget.setItem(row, 0, QTableWidgetItem(image_name))
                self.table_widget.setItem(row, 1, QTableWidgetItem(system))
                self.table_widget.setItem(row, 2, QTableWidgetItem(cer))
                self.table_widget.setItem(row, 3, QTableWidgetItem(wer))
                self.table_widget.setItem(row, 4, QTableWidgetItem(time_taken))
                row += 1

                if system not in system_averages:
                    system_averages[system] = {"CER": [], "WER": [], "Time": []}
                if isinstance(metric.get("CER"), (int, float)):
                    system_averages[system]["CER"].append(metric["CER"])
                if isinstance(metric.get("WER"), (int, float)):
                    system_averages[system]["WER"].append(metric["WER"])
                system_averages[system]["Time"].append(times[image_name].get(system, 0))

        for system, values in system_averages.items():
            cer_avg = sum(values["CER"]) / len(values["CER"]) if values["CER"] else 0
            wer_avg = sum(values["WER"]) / len(values["WER"]) if values["WER"] else 0
            time_avg = sum(values["Time"]) / len(values["Time"]) if values["Time"] else 0

            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem("overall_average"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(system))
            self.table_widget.setItem(row, 2, QTableWidgetItem(f"{cer_avg:.2f}"))
            self.table_widget.setItem(row, 3, QTableWidgetItem(f"{wer_avg:.2f}"))
            self.table_widget.setItem(row, 4, QTableWidgetItem(f"{time_avg:.2f}"))
            row += 1

        proxy_widget = self.scene.addWidget(self.table_widget)

        self.table_widget.setMinimumSize(self.view.width() - 20, self.view.height() - 20)
        proxy_widget.setPos(10, 10)

    def display_metrics_img(self, metrics):
        self.scene.clear()
        formatted_metrics = "\n".join(
            [f"{system} Metrics:\nCER: {metric['CER']:.2f}\nWER: {metric['WER']:.2f}"
             for system, metric in metrics.items()]
        )
        text_item = QGraphicsTextItem(formatted_metrics)
        font = QFont("Arial", 10)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
        text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)

    def export_metrics(self):
        if not self.table_widget:
            print("No metrics to export.")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Export Metrics", "", "CSV Files (*.csv)", options=options)
        if file_name:
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                writer.writerow(headers)
                for row in range(self.table_widget.rowCount()):
                    row_data = [self.table_widget.item(row, col).text() for col in range(self.table_widget.columnCount())]
                    writer.writerow(row_data)

    def export_results(self, ocr_results):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder to Save Results")
        if not folder:
            print("No folder selected. Export canceled.")
            return

        try:
            for image_name, systems_results in ocr_results.items():
                for system, result in systems_results.items():
                    file_name = f"{image_name}_{system}.txt"
                    file_path = os.path.join(folder, file_name)

                    with open(file_path, "w") as file:
                        file.write(f"Results for {image_name} using {system}:\n")
                        file.write(result)

            print(f"Results exported successfully to {folder}.")
        except Exception as e:
            print(f"An error occurred while exporting results: {e}")

    def export_image_results(self, ocr_results):
        if not ocr_results:
            print("No OCR results to export.")
            return
        try:
            folder = QFileDialog.getExistingDirectory(None, "Select Folder to Save Results")
            if not folder:
                print("No folder selected. Export canceled.")
                return

            for system, result in ocr_results.items():
                image_name = os.path.splitext(os.path.basename(self.image))[0] if self.image else "image"
                file_name = f"{image_name}_{system}.txt"
                file_path = os.path.join(folder, file_name)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(f"OCR System: {system}\n")
                    file.write(f"Result:\n{result}\n")
                    file.write("-" * 40 + "\n")

            print(f"OCR results successfully exported to {folder}.")
        except Exception as e:
            print(f"An error occurred while exporting results: {e}")

    def display_results_dtst(self, ocr_results, annotations):
        self.scene.clear()
        y_offset = 10
        max_width = 300

        for image_name, systems_results in ocr_results.items():
            annotation = annotations.get(image_name, "No annotation available")
            annotation_text = f"{image_name} Annotation:\n{annotation}\n{'-' * 40}"
            annotation_item = QGraphicsTextItem(annotation_text)
            font = QFont("Arial", 10)
            annotation_item.setFont(font)
            annotation_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
            annotation_item.setTextWidth(max_width)
            annotation_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.scene.addItem(annotation_item)
            annotation_item.setPos(10, y_offset)
            y_offset += annotation_item.boundingRect().height() + 10

            for system, result in systems_results.items():
                formatted_result = f"Results from {system}:\n{result}\n{'-' * 40}"
                text_item = QGraphicsTextItem(formatted_result)
                text_item.setFont(font)
                text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
                text_item.setTextWidth(max_width)
                text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                self.scene.addItem(text_item)
                text_item.setPos(10, y_offset)
                y_offset += text_item.boundingRect().height() + 10

    def display_results_img(self, ocr_results, annotation):
        self.scene.clear()
        y_offset = 10
        max_width = 300

        if annotation:
            annotation_text = f"Annotation:\n{annotation}\n{'-' * 40}"
            annotation_item = QGraphicsTextItem(annotation_text)
            font = QFont("Arial", 10)
            annotation_item.setFont(font)
            annotation_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
            annotation_item.setTextWidth(max_width)
            annotation_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.scene.addItem(annotation_item)
            annotation_item.setPos(10, y_offset)
            y_offset += annotation_item.boundingRect().height() + 10

        for system, result in ocr_results.items():
            formatted_result = f"Results from {system}:\n{result}\n{'-' * 40}"
            text_item = QGraphicsTextItem(formatted_result)
            font = QFont("Arial", 10)
            text_item.setFont(font)
            text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
            text_item.setTextWidth(max_width)
            text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.scene.addItem(text_item)
            text_item.setPos(10, y_offset)
            y_offset += text_item.boundingRect().height() + 10

    def add_background_text(self, text):
            text_item = QGraphicsTextItem(text)
            font = QFont("Arial", 16)
            text_item.setFont(font)
            text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
            self.scene.addItem(text_item)
            text_item.setPos(10, 10)

    def add_annotation_text(self, text):
        text_item = QGraphicsTextItem(text)
        font = QFont("Arial", 10)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
        text_item.setTextWidth(300)
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)

    def get_annotation(self):
        return self.annotation

    def get_image(self):
        return self.image

    def get_image_folder(self):
        return self.image_folder

    def get_annotation_folder(self):
        return self.annotation_folder