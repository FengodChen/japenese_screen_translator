from tkinter import *
from threading import Thread, Lock

class GUI_Main:
    def __init__(self, pipe_screenSelector, pipe_screenCropper):
        self.__pipe_screenSelector = pipe_screenSelector
        self.__pipe_orc_and_translate = pipe_screenCropper

        self.__create_main_windows()
    
    def run(self):
        self.__main_windows.mainloop()

    def __create_main_windows(self):
        self.__main_windows = Tk()
        self.__main_windows.title("Japenese Screen Translator")

        # Set Button 1
        self.__buttons_start_screenSelector = Button(
            self.__main_windows,
            text = "Select Pos",
            command = self.__start_screenSelector
        )
        self.__buttons_start_screenSelector.grid(column=0, row=0)

        # Set Button 2
        self.__buttons_start_ocr_and_translate = Button(
            self.__main_windows,
            text = "Start OCR and Translate",
            command = self.__start_ocr_and_translate,
            state = "disabled"
        )
        self.__buttons_start_ocr_and_translate.grid(column=0, row=1)
    
    def __start_screenSelector(self):
        msg = dict(
            comm = "start select",
            data = None
        )
        try:
            self.__pipe_screenSelector.send(msg)
            msg = self.__pipe_screenSelector.recv()
            if msg["comm"] == "push pos data":
                data = msg["data"]
                msg = dict(
                    comm = "set crop pos",
                    data = data
                )
                self.__pipe_orc_and_translate.send(msg)
                self.__buttons_start_ocr_and_translate.configure(state="normal")
        except Exception as e:
            print(str(e))
    
    def __start_ocr_and_translate(self):
        try:
            msg = dict(
                comm = "start ocr and translate",
                data = None
            )
            self.__pipe_orc_and_translate.send(msg)
            msg = self.__pipe_orc_and_translate.recv()
            if msg["comm"] == "push crop img":
                img = msg["data"]
                print(img)
        except:
            pass