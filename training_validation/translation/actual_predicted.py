from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
from datasets import load_dataset


raw_datasets = load_dataset("momo22/eng2nep")
test_subset = raw_datasets['test']

model_checkpoint = "logic/translation/models/model_kag2"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)


with open("logic/translation/actual_predicted/english.txt", "w", encoding="utf-8") as english_file, \
     open("logic/translation/actual_predicted/actual.txt", "w", encoding="utf-8") as actual_file, \
     open("logic/translation/actual_predicted/predicted.txt", "w", encoding="utf-8") as predicted_file:

    range_count = range(2000, 4000) # change the range
    start = range_count[0]
    end = range_count[-1]


    for i in range(start, end+1):
        
        example = test_subset[i]

        english_text = example["English"]
        actual_nepali_text = example["Nepali"]

        tokenized = tokenizer([english_text], return_tensors='np')
        output_ids = model.generate(**tokenized, max_length=128)
        predicted_nepali_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        english_file.write(english_text)
        actual_file.write(actual_nepali_text)
        predicted_file.write(predicted_nepali_text + "\n")

        print(f"{i}: completed")