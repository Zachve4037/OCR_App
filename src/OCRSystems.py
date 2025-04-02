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

    def ocr_ocrmypdf(self, input_pdf, dpi=300):
        # Create an output PDF path
        output_pdf = input_pdf.replace('.pdf', '_ocr.pdf')  # For PDFs
        if not input_pdf.endswith('.pdf'):  # If the input is an image, convert the image to a PDF
            output_pdf = input_pdf.replace('.jpg', '.pdf').replace('.png', '.pdf')  # Adjust as needed for other formats

        try:
            # Perform OCR and check if it returns something valid
            ocrmypdf.ocr(input_pdf, output_pdf, language='eng', image_dpi=dpi)

            # If OCRmyPDF was successful, print success message
            print(f"OCR completed successfully. Output saved to {output_pdf}")
            return output_pdf
        except Exception as e:
            print(f"Error during OCR process: {e}")
            return None

    def ocr_easyocr(self, image_path):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_path)
        return results

    def ocr_system2(self, image_path):
        return "OCR System 2 result"

    def ocr_system3(self, image_path):
        return "OCR System 3 result"

    def ocr_system4(self, image_path):
        return "OCR System 4 result"

    def perform_ocr(self, image_path):
        results = {
            #"Tesseract": self.ocr_tesseract(image_path),
            "OCRmyPDF": self.ocr_ocrmypdf(image_path),
            #"EasyOCR": self.ocr_easyocr(image_path),
        }
        return results
