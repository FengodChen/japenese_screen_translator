import torch
from utils import Translator, Screen_Cropper, Japenese_OCR, ScreenSelector

dev = torch.device("cuda:0")

ss = ScreenSelector()
sc = Screen_Cropper()
ocr = Japenese_OCR(dev=dev)
tr = Translator(src_lang="ja", target_lang="zh", dev=dev)

while True:
    ss.ui_show()
    (top_left, bottom_right) = ss.get_screen_pos()

    sc.set_crop_pos(top_left, bottom_right)
    img = sc.crop()

    ja_text = ocr.get_text(img)

    zh_text = tr.translate(ja_text)

    print("===========")
    print(ja_text)
    print(zh_text)
    _ = input("Enter to continue")

