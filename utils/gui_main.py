from tkinter import *
import time
from threading import Thread, Lock

class GUI_Main:
    def __init__(self, pipe_screenSelector, pipe_screenCropper, auto_run_time=0.5):
        self.__pipe_screenSelector = pipe_screenSelector
        self.__pipe_orc_and_translate = pipe_screenCropper

        self.__auto_run_flag = False
        self.__auto_run_time = auto_run_time
        self.__auto_run_last_run_time = time.time()

        self.__create_main_windows()
    
    def run(self):
        self.__main_windows.mainloop()
        self.__end_all()

    def __create_main_windows(self):
        self.__main_windows = Tk()
        self.__main_windows.geometry("600x300")
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
        self.__buttons_start_ocr_and_translate.grid(column=1, row=0)

        # Set Button 3
        self.__buttons_auto_run = Button(
            self.__main_windows,
            text = "Start Auto Run",
            command = self.__on_click_auto_run,
            state = "disabled"
        )
        self.__buttons_auto_run.grid(column=2, row=0)

        # Set Subtitle Label
        self.__label_subtitle = Label(self.__main_windows, text="<subtitle>")
        self.__label_subtitle.grid(column=0, row=1)
    
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
                self.__buttons_auto_run.configure(state="normal")
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
                data = msg["data"]
                ja_text = data[0]
                zh_text = data[1]
                text = f"{ja_text}\n{zh_text}"
                self.__label_subtitle.configure(text=text)
        except:
            pass
    
    def __on_click_auto_run(self):
        if self.__auto_run_flag == True:
            # stop "auto run"
            self.__auto_run_flag = False
            self.__buttons_auto_run.configure(text="Start Auto Run")
            self.__buttons_start_ocr_and_translate.configure(state="normal")
        else:
            # start "auto run"
            self.__auto_run_flag = True
            self.__auto_run_thread = Thread(
                target=self.__auto_run_task,
                daemon=True
            )
            self.__auto_run_thread.start()
            self.__buttons_auto_run.configure(text="Stop Auto Run")
            self.__buttons_start_ocr_and_translate.configure(state="disabled")
    
    def __auto_run_task(self):
        while self.__auto_run_flag == True:
            now_time = time.time()
            delta_time = now_time - self.__auto_run_last_run_time
            if delta_time < self.__auto_run_time:
                time.sleep(delta_time)
            
            self.__auto_run_last_run_time = time.time()
            self.__start_ocr_and_translate()
    
    def __end_all(self):
        self.__auto_run_flag = False

        msg = dict(
            comm = "end",
            data = None
        )

        self.__pipe_screenSelector.send(msg)
        self.__pipe_orc_and_translate.send(msg)