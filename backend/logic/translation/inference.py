import os

from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM

from gtts import gTTS
from io import BytesIO
import base64


model_checkpoint = "logic/translation/models/model_kag3"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)


def text_to_speech(nepali_text):
    tts = gTTS(text=nepali_text, lang='ne')
    # tts.save('logic/translation/outputs/output.wav')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
    return audio_base64


def en_ne_conversion(input_text):
    tokenized = tokenizer([input_text], return_tensors='np')
    out = model.generate(**tokenized, max_length=128)

    with tokenizer.as_target_tokenizer():
        output = tokenizer.decode(out[0], skip_special_tokens=True)

        # translation output in txt file
        # filename = "logic/translation/outputs/output.txt"
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(input_text+"\n")
        #     f.write(output)

        return output


# usage
# english_text = "Nepal is a beautiful country."
# nepali_text = en_ne_conversion(english_text)
# text_to_speech(nepali_text)