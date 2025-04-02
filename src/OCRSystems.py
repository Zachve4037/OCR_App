import img2pdf
import pytesseract
import ocrmypdf
import easyocr
from PIL import Image

class OCRSystem:
    def __init__(self):
        pass

    def ocr_tesseract(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang = 'eng')

    def image_to_pdf(self, image_path, pdf_path):
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_path))

    def ocr_ocrmypdf(self, input_pdf, output_pdf):
        ocrmypdf.ocr(input_pdf, output_pdf, language = 'eng')

    def ocr_easyocr(self, image_path):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_path)
        return results

    def ocr_system2(self, image_path):
        # Placeholder for the second OCR system
        return "OCR System 2 result"

    def ocr_system3(self, image_path):
        # Placeholder for the third OCR system
        return "OCR System 3 result"

    def ocr_system4(self, image_path):
        # Placeholder for the fourth OCR system
        return "OCR System 4 result"

    def perform_ocr(self, image_path):
        results = {
            "Tesseract": self.ocr_tesseract(image_path),
            "System2": self.ocr_system2(image_path),
            "System3": self.ocr_system3(image_path),
            "System4": self.ocr_system4(image_path)
        }
        return results
