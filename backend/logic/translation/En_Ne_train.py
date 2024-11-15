import sys
print("Python version:", sys.version)


import tensorflow as tf
import keras


print("TensorFlow version:", tf.__version__)
print("Keras version:", keras.__version__)


gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPUs detected: {[gpu.name for gpu in gpus]}")
else:
    print("No GPU detected.")


import os
import sys
import transformers
import tensorflow as tf
from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import AdamWeightDecay
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM


# model_checkpoint = "Helsinki-NLP/opus-mt-en-hi"
model_checkpoint = "translation/models/model_0"

raw_datasets = load_dataset("momo22/eng2nep")

train_subset = raw_datasets['train'].select(range(int(1591270/3)))
validation_subset = raw_datasets['validation'].select(range(int(198909/3)))
test_subset = raw_datasets['test']

raw_datasets = DatasetDict({
    'train': train_subset,
    'validation': validation_subset,
    'test': test_subset
})

print(raw_datasets['train'][10])

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

tokenizer("Hello, this is a sentence!")

tokenizer(["Hello, this is a sentence!", "This is another sentence."])

with tokenizer.as_target_tokenizer():
    print(tokenizer(["म धेरै ज्ञानी छु।"]))

max_input_length = 128
max_target_length = 128

source_lang = "English"
target_lang = "Nepali"


def preprocess_function(examples):
    inputs = [ex for ex in examples["English"]]
    targets = [ex for ex in examples["Nepali"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=max_target_length, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


preprocess_function(raw_datasets["train"][:2])

tokenized_datasets = raw_datasets.map(preprocess_function, batched=True)

model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

# use batch size according to your GPU VRAM memory size.
# resource limitation exception may arise.
batch_size = 2
learning_rate = 2e-5
weight_decay = 0.01
num_train_epochs = 1

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf")
generation_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf", pad_to_multiple_of=128)


train_dataset = model.prepare_tf_dataset(
    tokenized_datasets["train"],
    shuffle=True,
    collate_fn=data_collator,
)

validation_dataset = model.prepare_tf_dataset(
    tokenized_datasets["validation"],
    batch_size=batch_size,
    shuffle=False,
    collate_fn=data_collator,
)

generation_dataset = model.prepare_tf_dataset(
    tokenized_datasets["validation"],
    batch_size=1,
    shuffle=False,
    collate_fn=generation_data_collator,
)

optimizer = AdamWeightDecay(learning_rate=learning_rate, weight_decay_rate=weight_decay)
model.compile(optimizer=optimizer)

# training on GPU
with tf.device('/GPU:0'):
    model.fit(train_dataset, validation_data=validation_dataset, epochs=1)


save_path = "translation/models/model_random"
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
