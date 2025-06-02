# OCR application
is a simple application using several open source ocr systems listed below. 
App is implemented in Python 3.10.0 because of systems support. GUI is made by PyQT5. 
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
Executable file is included in the release section. It probably contains several
problems, because of the complexity of the application, size of the libraries 
and the fact that python is not for executable files. (fun fact, if pyinstaller
does not work for you, try nuitka (it took 4 hours to one build, but it worked and it
prints you the actual problems :DD)). It also contains console, so you can see the problems
if you encounter some of them. If you want to run the executable file, feel free to do so. 
I strongly suggest to pull the repository, create a virtual environment 
and then run the app. 
If you are encountering some problems with installing paddleocr, try installing this paddleocr==2.7.2
.