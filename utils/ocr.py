from manga_ocr import MangaOcr
from PIL.Image import Image
import torch

class MangaOcr_Mod(MangaOcr):
    def __init__(self, dev, pretrained_model_name_or_path='kha-white/manga-ocr-base'):
        super().__init__(pretrained_model_name_or_path=pretrained_model_name_or_path, force_cpu=True)
        self.model.to(dev)

class Japenese_OCR:
    def __init__(self, dev):
        self.ocr = MangaOcr_Mod(dev=dev)
    
    def get_text(self, image:Image):
        text = self.ocr(image)
        return text

if __name__ == "__main__":
    dev = torch.device("cuda:0")
    mocr = MangaOcr_Mod(dev)
    text = mocr("../test.png")
    print(text)