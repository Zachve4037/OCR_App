import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsTextItem

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

    def display_metrics_dtst(self, metrics):
        self.scene.clear()
        formatted_metrics = ""
        for image_name, systems_metrics in metrics.items():
            formatted_metrics += f"{image_name}:\n"
            for system, metric in systems_metrics.items():
                wer = f"{metric.get('WER'):.2f}" if isinstance(metric.get('WER'), (int, float)) else "N/A"
                cer = f"{metric.get('CER'):.2f}" if isinstance(metric.get('CER'), (int, float)) else "N/A"
                formatted_metrics += f"  {system}:\n    WER: {wer}\n    CER: {cer}\n"
            formatted_metrics += "\n"
        text_item = QGraphicsTextItem(formatted_metrics)
        font = QFont("Arial", 10)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)

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
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)

    def display_results_dtst(self, ocr_results):
        self.scene.clear()
        y_offset = 10
        max_width = 300
        for image_name, systems_results in ocr_results.items():
            image_name_item = QGraphicsTextItem(f"{image_name}:")
            font = QFont("Arial", 10)
            image_name_item.setFont(font)
            image_name_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
            self.scene.addItem(image_name_item)
            image_name_item.setPos(10, y_offset)
            y_offset += image_name_item.boundingRect().height() + 5

            for system, result in systems_results.items():
                system_name_item = QGraphicsTextItem(f"  {system}:")
                system_name_item.setFont(font)
                system_name_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
                self.scene.addItem(system_name_item)
                system_name_item.setPos(10, y_offset)
                y_offset += system_name_item.boundingRect().height() + 5
                wrapped_result = QGraphicsTextItem(result)
                wrapped_result.setFont(font)
                wrapped_result.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
                wrapped_result.setTextWidth(max_width)  # Set the maximum width
                self.scene.addItem(wrapped_result)
                wrapped_result.setPos(20, y_offset)
                y_offset += wrapped_result.boundingRect().height() + 10

    def display_results_img(self, ocr_results):
        self.scene.clear()
        y_offset = 10
        max_width = 300

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