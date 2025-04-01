from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

class Loader:
    def __init__(self, label):
        self.label = label

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)