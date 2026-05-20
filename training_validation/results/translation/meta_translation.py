from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Read English input
with open("translation/actual_predicted/english_4000.txt", encoding="utf-8") as f:
    english_lines = [line.strip() for line in f]

# ─── 2. Meta NLLB-200 (Free, Open Source) ─────────────────────────────────────
print("Loading NLLB model...")
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

nllb_translations = []
for i, line in enumerate(english_lines):
    if not line:
        nllb_translations.append("")
        continue
    inputs = tokenizer(line, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("npi_Deva"),  # Nepali
        max_length=512
    )
    result = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    nllb_translations.append(result)
    # if i % 100 == 0:
    print(f"  NLLB: {i}/{len(english_lines)}")

with open("translation/actual_predicted/nllb_4000.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(nllb_translations))
print("Saved: nllb_4000.txt")
