from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(650, 420, 600, 400)

        layout = QVBoxLayout()

        help_text = QLabel("""
        <h2>How to Use the OCR Application</h2>
        <p><b>1. Image Test:</b></p>
        <ul>
            <li>Click on the "Image Test" button in the main menu.</li>
            <li>Open an image using the "Open Image" button.</li>
            <li>Optionally, open an annotation file for testing accuracy using "Open Annotation" button.</li>
            <li>Select the OCR systems to test using the checkboxes.</li>
            <li>Click "Test" to perform OCR and view results.</li>
        </ul>
        <p><b>2. Dataset Test:</b></p>
        <ul>
            <li>Click on the "Dataset Test" button in the main menu.</li>
            <li>Open a folder of images using "Open Image Folder".</li>
            <li>Open a folder of annotations using "Open Image Folder".</li>
            <li>Images and annotation to image must have the same name.</li>
            <li>Click "Test" to perform OCR on the dataset and view results.</li>
        </ul>
        <p><b>3. Exporting Results:</b></p>
        <ul>
            <li>Use the "Export Results" button to save OCR results.</li>
            <li>Use the "Export Metrics" button to save evaluation metrics.</li>
        </ul>
        """)
        help_text.setWordWrap(True)
        layout.addWidget(help_text)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)