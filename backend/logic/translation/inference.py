import os

from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM

from gtts import gTTS



def text_to_speech(nepali_text):
    tts = gTTS(text=nepali_text, lang='ne')
    tts.save("translation/output/output.wav")


def en_ne_conversion(input_text):

    model_checkpoint = "translation/models/model_1"

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

    tokenized = tokenizer([input_text], return_tensors='np')
    out = model.generate(**tokenized, max_length=128)

    with tokenizer.as_target_tokenizer():
        output = tokenizer.decode(out[0], skip_special_tokens=True)

        # translation output in txt file
        filename = "translation/output/output.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(input_text+"\n")
            f.write(output)

        return output


# usage
# english_text = "The child screamed. A large yellow dog bounded across the yard."
# nepali_text = en_ne_conversion(english_text)
# text_to_speech(nepali_text)