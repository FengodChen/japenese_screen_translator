from .gui_main import GUI_Main
from .screen_selector import ScreenSelector
from .screen_cropper import Screen_Cropper
from .ocr import Japenese_OCR
from .translator import Translator

def gui_main_process(p1, p2):
    g = GUI_Main(p1, p2)
    g.run()

def screen_selector_subprocess(pipe_mainGUI):
    screen_selector = ScreenSelector()

    while True:
        try:
            msg = pipe_mainGUI.recv()
            if msg["comm"] == "start select":
                screen_selector.select_pos()
                pos_data = screen_selector.get_screen_pos()
                msg = dict(
                    comm = "push pos data",
                    data = pos_data
                )
                pipe_mainGUI.send(msg)
            elif msg["comm"] == "end":
                break
        except Exception as e:
            print(str(e))

def orc_translate_subprocess(dev, pipe_mainGUI):
    screen_cropper = Screen_Cropper()
    japenese_ocr = Japenese_OCR(dev=dev)
    translator = Translator(src_lang="ja", target_lang="zh", dev=dev)

    while True:
        try:
            msg = pipe_mainGUI.recv()
            if msg["comm"] == "start ocr and translate":
                img = screen_cropper.crop()
                ja_text = japenese_ocr.get_text(img)
                zh_text = translator.translate(ja_text)
                msg = dict(
                    comm = "push crop img",
                    data = (ja_text, zh_text)
                )
                pipe_mainGUI.send(msg)
            elif msg["comm"] == "set crop pos":
                (top_left, bottom_right) = msg["data"]
                screen_cropper.set_crop_pos(top_left, bottom_right)
            elif msg["comm"] == "end":
                break
        except Exception as e:
            print(str(e))