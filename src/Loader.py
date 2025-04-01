from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsTextItem


class Loader:
    def __init__(self, view, text):
        self.view = view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.add_background_text(text)

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.view.fitInView(self.scene.itemsBoundingRect(), mode=1)

    def add_background_text(self, text):
        text_item = QGraphicsTextItem(text)
        font = QFont("Arial", 16)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor.fromRgb(238, 244, 237))
        self.scene.addItem(text_item)
        text_item.setPos(10, 10)
