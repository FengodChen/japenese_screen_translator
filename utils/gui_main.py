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

        self.__font_size = 20
        self.__font_style = "Arial"

        self.__show_ja = True
        self.__show_zh = True

        self.__create_main_windows()
    
    def run(self):
        self.__main_windows.mainloop()
        self.__end_all()

    def __get_width(self):
        return self.__main_windows.winfo_width()
    
    def __increase_font_size(self):
        self.__font_size += 2
        self.__label_subtitle.configure(font=(self.__font_style, self.__font_size))

    def __decrease_font_size(self):
        self.__font_size -= 2
        self.__font_size = max(0, self.__font_size)
        self.__label_subtitle.configure(font=(self.__font_style, self.__font_size))
    
    def __on_click_show_ja(self):
        if self.__show_ja:
            self.__show_ja = False
            self.__buttons_show_ja.configure(text="启用日语")
        else:
            self.__show_ja = True
            self.__buttons_show_ja.configure(text="禁用日语")

    def __on_click_show_zh(self):
        if self.__show_zh:
            self.__show_zh = False
            self.__buttons_show_zh.configure(text="启用中文")
        else:
            self.__show_zh = True
            self.__buttons_show_zh.configure(text="禁用中文")

    def __create_main_windows(self):
        self.__main_windows = Tk()
        self.__main_windows.geometry("600x300")
        self.__main_windows.title("日语屏幕翻译器")
        self.__main_windows.columnconfigure(0, weight=1)
        self.__main_windows.rowconfigure(0, weight=1)

        # Set Buttom Lable
        self.__buttom_label = Label(
            self.__main_windows,
            pady = 30
        )
        self.__buttom_label.grid(column=0, row=1)

        # Set Button Select Pos
        self.__buttons_start_screenSelector = Button(
            self.__buttom_label,
            text = "选择翻译区域",
            command = self.__start_screenSelector
        )
        self.__buttons_start_screenSelector.grid(column=0, row=0)

        # Set Button Run
        self.__buttons_start_ocr_and_translate = Button(
            self.__buttom_label,
            text = "运行",
            command = self.__start_ocr_and_translate,
            state = "disabled"
        )
        self.__buttons_start_ocr_and_translate.grid(column=1, row=0)

        # Set Button Auto Run
        self.__buttons_auto_run = Button(
            self.__buttom_label,
            text = "自动运行",
            command = self.__on_click_auto_run,
            state = "disabled"
        )
        self.__buttons_auto_run.grid(column=2, row=0)

        # Set Font Setting Layer
        self.__font_setting_layer = Label(
            self.__buttom_label,
            padx=20
        )
        self.__font_setting_layer.grid(column=3, row=0)

        self.__buttons_decrease_font_size = Button(
            self.__font_setting_layer,
            text = "-",
            command = self.__decrease_font_size
        )
        self.__buttons_decrease_font_size.grid(column=0, row=0)

        self.__font_setting_hint = Label(
            self.__font_setting_layer,
            text="字幕大小"
        )
        self.__font_setting_hint.grid(column=1, row=0)

        self.__buttons_increase_font_size = Button(
            self.__font_setting_layer,
            text = "+",
            command = self.__increase_font_size
        )
        self.__buttons_increase_font_size.grid(column=2, row=0)

        # Set Button JA
        self.__buttons_show_ja = Button(
            self.__buttom_label,
            text = "禁用日语",
            command = self.__on_click_show_ja,
        )
        self.__buttons_show_ja.grid(column=4, row=0)

        # Set Button ZH
        self.__buttons_show_zh = Button(
            self.__buttom_label,
            text = "禁用中文",
            command = self.__on_click_show_zh,
        )
        self.__buttons_show_zh.grid(column=5, row=0)

        # Set Subtitle Label
        self.__label_subtitle = Label(
            self.__main_windows,
            text="<字幕区域>",
            font=(self.__font_style, self.__font_size),
            wraplength=600
        )
        self.__label_subtitle.grid(column=0, row=0)
    
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

                if self.__show_ja and self.__show_zh:
                    text = f"{ja_text}\n\n{zh_text}"
                elif self.__show_ja:
                    text = ja_text
                elif self.__show_zh:
                    text = zh_text
                else:
                    text = "<设置中即不显示日语也不显示中文>"
                self.__label_subtitle.configure(text=text, wraplength=self.__get_width())
        except:
            pass
    
    def __on_click_auto_run(self):
        if self.__auto_run_flag == True:
            # stop "auto run"
            self.__auto_run_flag = False
            self.__buttons_auto_run.configure(text="自动运行")
            self.__buttons_start_ocr_and_translate.configure(state="normal")
        else:
            # start "auto run"
            self.__auto_run_flag = True
            self.__auto_run_thread = Thread(
                target=self.__auto_run_task,
                daemon=True
            )
            self.__auto_run_thread.start()
            self.__buttons_auto_run.configure(text="停止运行")
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