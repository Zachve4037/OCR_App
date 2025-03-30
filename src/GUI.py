import tkinter as tk


class GUI:
    def __init__(self):
        # Main window setup
        self.mainWin = tk.Tk()
        self.mainWin.geometry("1080x640")
        self.mainWin.title("OCR_App")

        # Configure the grid to center content
        self.mainWin.grid_columnconfigure(0, weight=1)

        # Create frames
        self.main_frame = tk.Frame(self.mainWin)
        self.ocr_frame = tk.Frame(self.mainWin)
        self.test_frame = tk.Frame(self.mainWin)

        for frame in (self.main_frame, self.ocr_frame, self.test_frame):
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)  # Center column in each frame

        self.main_menu()
        self.mainWin.mainloop()

    def main_menu(self):
        self.clear_frame(self.main_frame)
        self.main_frame.tkraise()

        # Configure the main frame's grid
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self.main_frame, text="Welcome to OCR Application", font=("Arial", 25, "bold"))
        self.label.grid(pady=10)

        self.description = tk.Label(self.main_frame,
                                    text="OCR System - Extract text from images\nOCR Testing - Test the OCR performance",
                                    font=("Arial", 16))
        self.description.grid(pady=10)

        self.btn_style = {"font": ("Arial", 12, "bold"), "height": 2, "width": 20}

        # Create a container frame for buttons to center them together
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(pady=20)

        self.OCRSysButton = tk.Button(self.button_frame, text="OCR System", **self.btn_style, command=self.ocr_menu)
        self.OCRSysButton.grid(pady=10)

        self.TestingButton = tk.Button(self.button_frame, text="OCR Testing", **self.btn_style,
                                       command=self.testing_menu)
        self.TestingButton.grid(pady=10)

    def ocr_menu(self):
        self.clear_frame(self.ocr_frame)
        self.ocr_frame.tkraise()

        # Configure the OCR frame's grid
        self.ocr_frame.grid_columnconfigure(0, weight=1)

        self.ocr_label = tk.Label(self.ocr_frame, text="OCR System", font=("Arial", 20, "bold"))
        self.ocr_label.grid(pady=20)

        # Create a container frame for buttons
        self.button_frame = tk.Frame(self.ocr_frame)
        self.button_frame.grid(pady=20)

        self.upload_btn = tk.Button(self.button_frame, text="Upload Image", **self.btn_style)
        self.upload_btn.grid(pady=10)

        self.back_btn = tk.Button(self.button_frame, text="Back to Main", **self.btn_style, command=self.main_menu)
        self.back_btn.grid(pady=20)

    def testing_menu(self):
        self.clear_frame(self.test_frame)
        self.test_frame.tkraise()

        # Configure the test frame's grid
        self.test_frame.grid_columnconfigure(0, weight=1)

        self.test_label = tk.Label(self.test_frame, text="OCR Testing", font=("Arial", 20, "bold"))
        self.test_label.grid(pady=20)

        # Create a container frame for buttons
        self.button_frame = tk.Frame(self.test_frame)
        self.button_frame.grid(pady=20)

        self.back_btn = tk.Button(self.button_frame, text="Back to Main", **self.btn_style, command=self.main_menu)
        self.back_btn.grid(pady=20)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()