# OCR application
is a simple application using several open source ocr systems listed below. 
App is implemented in Python 3.10.0 because of systems support. GUI is made by PyQT. 
This app lets you to either perform ocr on your input file or test included 
systems with your input and annotation of the input. Tests can be performed
on single image or on a directory with images.
## Bachelor's thesis:
OCR Solutions for Text Recognition in Real-World Scenes and Structured Documents
# OCR Systems included in application
Tesseract - Structured documents

OCRmyPDF - Structured documents 

EasyOCR - Real-world scenes

PaddleOCR - Real-world scenes and structured documents

Please note that the systems does not support GPU usage so app runs only on CPU.
Based on that information, assume that it takes some time to perform test 
(roughly 30 seconds per image). If you want to perform only text extraction
I suggest using paddle ocr or tesseract since they are the fastest ones.

# Installation
I have added the executable file to the repository. I suggest using it only if you are
not able to pull the repository and run the project by your self. The exe takes time
to start (roughly 30 seconds), because of large libraries and models of OCR systems,
but it will run (maybe). The python was not developed 
for exe usage so I am not sure if it will work. So if you can, pull the repository
and download the necessary dependencies.