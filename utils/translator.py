import torch
from torch import Tensor
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class Translator:
    def __init__(self, src_lang, target_lang, dev):
        self.dev = dev

        self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(self.dev).eval()
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

        self.src_lang = src_lang
        self.target_lang = self.tokenizer.get_lang_id(target_lang)
        self.tokenizer.src_lang = src_lang

    def translate(self, input_text):
        encoded_zh = self.tokenizer(input_text, return_tensors="pt")

        input_ids:Tensor = encoded_zh["input_ids"]
        attention_mask:Tensor = encoded_zh["attention_mask"]

        input_ids = input_ids.to(self.dev)
        attention_mask = attention_mask.to(self.dev)

        with torch.no_grad():
            generated_tokens = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, forced_bos_token_id=self.target_lang)
            translate_ans = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        
        assert len(translate_ans) == 1
        return translate_ans[0]

if __name__ == "__main__":
    translator = Translator(
        src_lang="zh",
        target_lang="ja",
        gpu_num=0
    )

    chinese_text = "生活就像一盒巧克力。"
    ans = translator.translate(chinese_text)
    print(ans)
