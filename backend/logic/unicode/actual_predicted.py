import os
from datasets import load_dataset
from inference import predict_output

# Load the dataset
ds = load_dataset("Saugatkafley/Nepali-Roman-Transliteration")

with open("logic/unicode/actual_predicted/nepali.txt", "w", encoding="utf-8") as nepali_file, \
     open("logic/unicode/actual_predicted/actual.txt", "w", encoding="utf-8") as actual_file:
     
    for example in ds['validation']:
        native_word = example['native word']
        english_word = example['english word']
        
        nepali_file.write(native_word + '\n')
        actual_file.write(english_word + '\n')

    print("Files created: nepali.txt, actual.txt")


native_list = []
with open("logic/unicode/actual_predicted/nepali.txt", 'r', encoding='utf-8') as file:
    for line in file:
        native_list.append(line.strip())

with open("logic/unicode/actual_predicted/predicted.txt", "w", encoding="utf-8") as predicted_file:
    for native_word in native_list:
        predicted_word = predict_output(native_word)
        predicted_file.write(predicted_word + '\n')
