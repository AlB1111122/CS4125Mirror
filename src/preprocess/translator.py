from abc import ABC
import stanza
from stanza.pipeline.core import DownloadMethod
from transformers import pipeline
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class ITranslator(ABC):
    def __init__(self, lang):
        self.lang = lang
        pass
    def translate(self, texts):
        pass

    def map_language(self, lang):
        pass

class StanzaTranslator(ITranslator):
    def __init__(self,lang):
        super().__init__(lang)
        self.t2t_m = "facebook/m2m100_418M"
        self.t2t_pipe = pipeline(task='text2text-generation', model=self.t2t_m)
        self.trans_model = M2M100ForConditionalGeneration.from_pretrained(self.t2t_m)
        self.tokenizer = M2M100Tokenizer.from_pretrained(self.t2t_m)
        self.nlp_stanza = stanza.Pipeline(lang="multilingual", processors="langid",
                                 download_method=DownloadMethod.REUSE_RESOURCES)
        self.mappings = {
        "fro": "fr",
        "la": "it",
        "nn": "no",
        "kmr": "tr"
        }

    def map_language(self, lang):
        if(lang in self.mappings.keys()):
            return self.mappings[lang]

    def translate(self, texts):
        text_transd_l = []
        for text in texts:
            if text == "":
                text_transd_l = text_transd_l + [text]
                continue

            doc = self.nlp_stanza(text)
            print(doc.lang)
            if doc.lang == self.lang:
                text_transd_l = text_transd_l + [text]
            else:
                self.map_language(doc.lang)
                case = 2

                if case == 1:
                    text_transd = self.t2t_pipe(text, forced_bos_token_id=self.tokenizer.get_lang_id(lang=self.lang))
                    text_transd = text_transd[0]['generated_text']
                elif case == 2:
                    self.tokenizer.src_lang = doc.lang
                    encoded_hi = self.tokenizer(text, return_tensors="pt")
                    generated_tokens = self.trans_model.generate(**encoded_hi,
                                                                 forced_bos_token_id=self.tokenizer.get_lang_id(self.lang))
                    text_transd = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
                    text_transd = text_transd[0]
                else:
                    text_transd = text

                text_transd_l = text_transd_l + [text_transd]

                print(text)
                print(text_transd)

        return text_transd_l