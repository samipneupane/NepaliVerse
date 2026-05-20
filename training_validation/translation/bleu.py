import evaluate

bleu = evaluate.load("sacrebleu")

print("Start")

with open("logic/translation/actual_predicted/actual_4000.txt", "r", encoding="utf-8") as f:
    references = [[line.strip()] for line in f]

with open("logic/translation/actual_predicted/predicted_4000.txt", "r", encoding="utf-8") as f:
    predictions = [line.strip() for line in f]

# Compute BLEU score
results = bleu.compute(predictions=predictions, references=references)

print("BLEU score:", results['score']/100)
