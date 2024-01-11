import torch
from multiprocessing import Pipe, Process
from utils import Translator, Screen_Cropper, Japenese_OCR, ScreenSelector
from utils.screen_selector import screen_selector_process
from utils.gui_main import GUI_Main
from time import sleep

"""
dev = torch.device("cuda:0")

ss = ScreenSelector()
sc = Screen_Cropper()
ocr = Japenese_OCR(dev=dev)
tr = Translator(src_lang="ja", target_lang="zh", dev=dev)

ss.select_pos()
(top_left, bottom_right) = ss.get_screen_pos()

sc.set_crop_pos(top_left, bottom_right)
img = sc.crop()

ja_text = ocr.get_text(img)

zh_text = tr.translate(ja_text)
"""

def gui_main(p1, p2):
    g = GUI_Main(p1, p2)
    g.run()

def orc_translate_process(dev, pipe_mainGUI):
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


if __name__ == "__main__":
    dev = torch.device(f"cuda:0")
    pipe1_main_selec, pipe2_main_selec = Pipe()
    pipe1_main_ocrTrans, pipe2_main_ocrTrans = Pipe()

    process_main = Process(target=gui_main, args=(pipe1_main_selec, pipe1_main_ocrTrans))
    process_selector = Process(target=screen_selector_process, args=(pipe2_main_selec, ))
    process_ocr_translate = Process(target=orc_translate_process, args=(dev, pipe2_main_ocrTrans, ))

    process_main.start()
    process_selector.start()
    process_ocr_translate.start()
    process_main.join()
    process_selector.join()
    process_ocr_translate.join()