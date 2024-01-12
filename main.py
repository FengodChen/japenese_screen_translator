import torch
from multiprocessing import Pipe, Process
from utils import gui_main_process, screen_selector_subprocess, orc_translate_subprocess

if __name__ == "__main__":
    dev = torch.device(f"cuda:0")
    #dev = torch.device("cpu")
    pipe1_main_selec, pipe2_main_selec = Pipe()
    pipe1_main_ocrTrans, pipe2_main_ocrTrans = Pipe()

    process_main = Process(target=gui_main_process, args=(pipe1_main_selec, pipe1_main_ocrTrans))
    process_selector = Process(target=screen_selector_subprocess, args=(pipe2_main_selec, ))
    process_ocr_translate = Process(target=orc_translate_subprocess, args=(dev, pipe2_main_ocrTrans, ))

    process_main.start()
    process_selector.start()
    process_ocr_translate.start()

    process_main.join()