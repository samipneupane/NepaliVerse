import ntr
from indic_transliteration import sanscript

with open("transliteration/actual_predicted/nepali_all.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f]

# ─── Baseline 1: nepali-to-roman ──────────────────────────────────────────────
ntr_results = []
for i, line in enumerate(input_lines):
    try:
        ntr_results.append(ntr.nep_to_rom(line) if line else "")
    except Exception as e:
        print(f"ntr error at line {i}: {e}")
        ntr_results.append("")

with open("transliteration/actual_predicted/ntr_all.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(ntr_results))
print("Saved: ntr_all.txt")


# ─── Baseline 2: indic-transliteration (IAST scheme) ─────────────────────────
iast_results = []
for i, line in enumerate(input_lines):
    try:
        result = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.ITRANS) if line else ""
        iast_results.append(result.lower())
    except Exception as e:
        print(f"IAST error at line {i}: {e}")
        iast_results.append("")

with open("transliteration/actual_predicted/iast_all.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(iast_results))
print("Saved: iast_all.txt")