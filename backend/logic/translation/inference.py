import os

from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM

from gtts import gTTS

from pydub import AudioSegment


def text_to_speech(nepali_text):
    tts = gTTS(text=nepali_text, lang='ne')
    if not os.path.exists("media"):
        os.makedirs("media")
    tts.save("media/output.wav")

def en_ne_conversion(input_text):

    model_checkpoint = "logic/translation/models/model_1"

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

    tokenized = tokenizer([input_text], return_tensors='np')
    out = model.generate(**tokenized, max_length=128)

    with tokenizer.as_target_tokenizer():
        output = tokenizer.decode(out[0], skip_special_tokens=True)

        # translation output in txt file
        # filename = "logic/translation/output/output.txt"
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(input_text+"\n")
        #     f.write(output)

        return output


# usage
# english_text = "Nepal is very beautiful country. I love my country very much. Many tourist come and explore Nepal."
# nepali_text = en_ne_conversion(english_text)
# text_to_speech(nepali_text)