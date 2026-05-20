import evaluate

print("Loading metrics...")

bleu    = evaluate.load("sacrebleu")
chrf    = evaluate.load("chrf")
ter     = evaluate.load("ter")
bertscore = evaluate.load("bertscore")
meteor  = evaluate.load("meteor")

print("Reading files...")

with open("translation/actual_predicted/actual_4000.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f]
    references_list  = [[line] for line in lines]   # for BLEU, chrF, TER
    references_flat  = lines                         # for METEOR, BERTScore

with open("translation/actual_predicted/nllb_4000.txt", encoding="utf-8") as f:
    predictions = [line.strip() for line in f]

print("Computing metrics...")

bleu_result     = bleu.compute(predictions=predictions, references=references_list)
print("BLEU computed")
chrf_result     = chrf.compute(predictions=predictions, references=references_list)
print(f"chrF computed")
ter_result      = ter.compute(predictions=predictions,  references=references_list)
print(f"TER computed")
bertscore_result= bertscore.compute(predictions=predictions, references=references_flat, lang="ne")
print(f"BERTScore F1 computed")
meteor_result   = meteor.compute(predictions=predictions, references=references_flat)
print(f"METEOR computed")

print(f"BLEU:         {bleu_result['score']:.2f}")
print(f"chrF:         {chrf_result['score']:.2f}")
print(f"TER:          {ter_result['score']:.2f}")
print(f"BERTScore F1: {sum(bertscore_result['f1'])/len(bertscore_result['f1']):.4f}")
print(f"METEOR:       {meteor_result['meteor']:.4f}")

breakpoint()