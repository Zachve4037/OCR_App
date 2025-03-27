import tkinter as tk

mainWin = tk.Tk()
mainWin.geometry("1080x640")
mainWin.title("OCR_App")

label = tk.Label(mainWin, text="Welcome to //TODO APP NAME", font=("Arial", 20))
label.pack(padx=5, pady=15)

description = tk.Label(mainWin, text="OCR System - Extract text from images \n OCR Testing - Test the OCR performance", font=("Arial", 20))
description.pack(padx=5, pady=5)

OCRSysButton = tk.Button(mainWin, text="OCR System", command=mainWin.destroy, font=("Arial", 10), height=5, width=25)
TestingButton = tk.Button(mainWin, text="OCR Testing", command=mainWin.destroy, font=("Arial", 10), height=5, width=25)


OCRSysButton.pack(padx=100, pady=60)
TestingButton.pack(padx=100, pady=10)

mainWin.mainloop()