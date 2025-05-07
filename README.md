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
I tried to make executable file, I made it but it is too big to upload it here. 
So your only option is to pull the repository, download the necessary libraries
and dependencies and then run the app. If you need help with that, please
contact me :D.