import torch
from multiprocessing import Pipe, Process
from utils import Translator, Screen_Cropper, Japenese_OCR, ScreenSelector
from utils.screen_selector import screen_selector_process
from utils.screen_cropper import screen_cropper_process
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


if __name__ == "__main__":
    p1, p2 = Pipe()
    p3, p4 = Pipe()
    process1 = Process(target=screen_selector_process, args=(p2, ))
    process2 = Process(target=gui_main, args=(p1, p3))
    process3 = Process(target=screen_cropper_process, args=(p4, None, ))

    process1.start()
    process2.start()
    process3.start()
    process1.join()
    process2.join()
    process3.join()