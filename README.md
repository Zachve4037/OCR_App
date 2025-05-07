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
There is a executable file included in the repository named Main.exe. I strongly
suggest pulling the whole git repository and running the app from your local machine.
The app might have some issues due to the fact that the python is not recommended
for executable files. I only made the executable file for the purpose of my Bc Thesis.
However, if you want to use the app and you run into some issues, please run the app
from the source code. If you run the app from the executable file, please note
that is has large libraries and models in it because of the OCR systems, so it will
take several time to load the app. (the executable file is 500MB). The app has
3.6GB give or take.