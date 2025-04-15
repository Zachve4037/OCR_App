import os
import shutil
import PyPDF2
import img2pdf
import pytesseract
import ocrmypdf
import easyocr
from PIL import Image
from paddleocr import PaddleOCR

class OCRSystem:
    def __init__(self):
        pass

    def ocr_tesseract(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang = 'eng')

    def image_to_pdf(self, image_path, pdf_path):
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_path))

    def ocr_ocrmypdf(self, input_pdf, output_pdf=None, dpi=300):
        if output_pdf is None:
            output_pdf = input_pdf.rsplit('.', 1)[0] + "_OCR.pdf"
        if not input_pdf.endswith('.pdf'):
            temp_input = input_pdf.rsplit('.', 1)[0] + "_temp." + input_pdf.rsplit('.', 1)[1]
            if temp_input == input_pdf:
                temp_input = input_pdf.rsplit('.', 1)[0] + "_copy." + input_pdf.rsplit('.', 1)[1]
            shutil.copy(input_pdf, temp_input)
        else:
            temp_input = input_pdf
        try:
            ocrmypdf.ocr(temp_input, output_pdf, language='eng', image_dpi=dpi)
            print(f"OCR completed successfully. Extracting text from {output_pdf}...")
            extracted_text = ""
            with open(output_pdf, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text += page.extract_text()
            return extracted_text
        except Exception as e:
            print(f"Error during OCR process: {e}")
            return None
        finally:
            if temp_input != input_pdf and os.path.exists(temp_input):
                os.remove(temp_input)

    def ocr_easyocr(self, image_path):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_path)
        extracted_text = ' '.join([result[1] for result in results])
        return extracted_text

    def ocr_paddleocr(self, image_path):
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        result = ocr.ocr(image_path, det=True, rec=True)
        extracted_text = []
        for line in result[0]:
            extracted_text.append(line[1][0])

        return ' '.join(extracted_text)

    def perform_ocr(self, image_path):
        results = {
            "Tesseract": self.ocr_tesseract(image_path),
            "OCRmyPDF": self.ocr_ocrmypdf(image_path, output_pdf="OCRmyPDF.pdf", dpi=300),
            "EasyOCR": self.ocr_easyocr(image_path),
            "PaddleOCR": self.ocr_paddleocr(image_path)
        }
        return results
