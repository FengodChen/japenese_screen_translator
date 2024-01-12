from .gui_main import GUI_Main
from .screen_selector import ScreenSelector
from .screen_cropper import Screen_Cropper
from .ocr import Japenese_OCR
from .translator import Translator

import torch
from torchvision.transforms import ToTensor

__to_tensor = ToTensor()

def __judge_diff(img1, img2):
    img1 = __to_tensor(img1) if img1 != None else torch.zeros(1)
    img2 = __to_tensor(img2)

    if img1.size() != img2.size():
        mse = 1e12
    else:
        mse = (img1 - img2).pow(2).mean().item()
    return mse

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

    pre_img = None
    pre_ja_text = ""
    pre_zh_text = ""
    MIN_MSE = 0.0001

    while True:
        try:
            msg = pipe_mainGUI.recv()
            if msg["comm"] == "start ocr and translate":
                img = screen_cropper.crop()
                if __judge_diff(pre_img, img) > MIN_MSE:
                    ja_text = japenese_ocr.get_text(img)
                    zh_text = translator.translate(ja_text)
                    pre_ja_text = ja_text
                    pre_zh_text = zh_text
                else:
                    ja_text = pre_ja_text
                    zh_text = pre_zh_text
                pre_img = img
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