from comet import download_model, load_from_checkpoint

print("Loading COMET model...")

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

data = []

with open("translation/actual_predicted/actual_4000.txt", encoding="utf-8") as ref_f, \
     open("translation/actual_predicted/predicted_4000.txt", encoding="utf-8") as pred_f, \
     open("translation/actual_predicted/english_4000.txt", encoding="utf-8") as eng_f:

    for eng, ref, pred in zip(eng_f, ref_f, pred_f):
        data.append({
            "src": eng.strip(),
            "mt": pred.strip(),
            "ref": ref.strip()
        })

print("Running COMET...")
model_output = model.predict(data, batch_size=8, gpus=0)

print(f"COMET score: {model_output.system_score:.4f}")

breakpoint()