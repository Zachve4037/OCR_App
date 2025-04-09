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

    def display_metrics(self, metrics):
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

    def display_results(self, ocr_results):
        self.scene.clear()
        y_offset = 10
        for system, result in ocr_results.items():
            formatted_result = f"Results from {system}:\n{result}\n{'-' * 40}"
            text_item = QGraphicsTextItem(formatted_result)
            font = QFont("Arial", 10)
            text_item.setFont(font)
            text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
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
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)

    def get_annotation(self):
        return self.annotation

    def get_image(self):
        return self.image