from deep_translator import GoogleTranslator
import time
import json

# Read English input
with open("translation/actual_predicted/english_4000.txt", encoding="utf-8") as f:
    english_lines = [line.strip() for line in f]


# ─── 1. Google Translate ───────────────────────────────────────────────────────
print("Running Google Translate...")
google_translations = []
error_lines = {}
translator = GoogleTranslator(source='en', target='ne')

for i, line in enumerate(english_lines):
    success = False
    for attempt in range(3):
        try:
            result = translator.translate(line[:4500]) if line else ""
            google_translations.append(result or "")
            success = True
            break
        except Exception as e:
            print(f"Google error at line {i} (attempt {attempt+1}/3): {e}")
            time.sleep(1 * (attempt + 1))  # wait 1s, 2s, 3s between retries

    if not success:
        google_translations.append("")
        error_lines[i] = line
        print(f"  Line {i} failed after 3 attempts — leaving blank.")

    print(f"  Google: {i}/{len(english_lines)}")
    time.sleep(1)

with open("translation/actual_predicted/google_4000.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(google_translations))
print("Saved: google_4000.txt")

with open("translation/actual_predicted/google_errors.json", "w", encoding="utf-8") as f:
    json.dump(error_lines, f, ensure_ascii=False, indent=2)
print(f"Saved: google_errors.json ({len(error_lines)} errors)")
