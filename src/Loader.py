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