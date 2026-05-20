import editdistance
from jiwer import wer
import numpy as np

def load_files(actual_file, predicted_file):
    with open(actual_file, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f.readlines()]
    with open(predicted_file, 'r', encoding='utf-8') as f:
        predicted_lines = [line.strip() for line in f.readlines()]
    if len(actual_lines) != len(predicted_lines):
        raise ValueError("Files must have the same number of lines.")
    return actual_lines, predicted_lines


def calculate_cer(actual_lines, predicted_lines):
    total_chars = 0
    total_errors = 0
    for a, p in zip(actual_lines, predicted_lines):
        total_errors += editdistance.eval(a, p)
        total_chars += len(a)
    return total_errors / total_chars if total_chars > 0 else 0


def calculate_wer(actual_lines, predicted_lines):
    return wer(actual_lines, predicted_lines)


def calculate_top1_accuracy(actual_lines, predicted_lines):
    correct = sum(1 for a, p in zip(actual_lines, predicted_lines) if a == p)
    return correct / len(actual_lines)


def calculate_precision_recall_f1(actual_lines, predicted_lines):
    precisions, recalls, f1s = [], [], []
    for a, p in zip(actual_lines, predicted_lines):
        a_chars = set(a)
        p_chars = set(p)
        if not p_chars:
            precisions.append(0)
            recalls.append(0)
            f1s.append(0)
            continue
        tp = len(a_chars & p_chars)
        precision = tp / len(p_chars) if p_chars else 0
        recall = tp / len(a_chars) if a_chars else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    return np.mean(precisions), np.mean(recalls), np.mean(f1s)


def calculate_mean_edit_distance(actual_lines, predicted_lines):
    distances = [editdistance.eval(a, p) for a, p in zip(actual_lines, predicted_lines)]
    return np.mean(distances)


def calculate_normalized_edit_distance(actual_lines, predicted_lines):
    scores = []
    for a, p in zip(actual_lines, predicted_lines):
        max_len = max(len(a), len(p))
        if max_len == 0:
            scores.append(0)
            continue
        scores.append(editdistance.eval(a, p) / max_len)
    return np.mean(scores)


def calculate_sequence_accuracy(actual_lines, predicted_lines):
    # Percentage of words where ALL characters match exactly
    return calculate_top1_accuracy(actual_lines, predicted_lines)


def calculate_partial_match(actual_lines, predicted_lines, threshold=0.8):
    # Percentage of predictions with normalized edit distance <= (1 - threshold)
    count = 0
    for a, p in zip(actual_lines, predicted_lines):
        max_len = max(len(a), len(p))
        if max_len == 0:
            count += 1
            continue
        similarity = 1 - editdistance.eval(a, p) / max_len
        if similarity >= threshold:
            count += 1
    return count / len(actual_lines)


# ─── Run all metrics ───────────────────────────────────────────────────────────

actual_file    = 'transliteration/actual_predicted/actual_all.txt'
predicted_file = 'transliteration/actual_predicted/ntr_all.txt'

actual_lines, predicted_lines = load_files(actual_file, predicted_file)

cer             = calculate_cer(actual_lines, predicted_lines)
wer_score       = calculate_wer(actual_lines, predicted_lines)
top1_acc        = calculate_top1_accuracy(actual_lines, predicted_lines)
precision, recall, f1 = calculate_precision_recall_f1(actual_lines, predicted_lines)
mean_ed         = calculate_mean_edit_distance(actual_lines, predicted_lines)
norm_ed         = calculate_normalized_edit_distance(actual_lines, predicted_lines)
partial_match   = calculate_partial_match(actual_lines, predicted_lines, threshold=0.8)

print("===== TRANSLITERATION EVALUATION RESULTS =====")
print(f"CER (Character Error Rate):         {cer:.4f}  (lower is better)")
print(f"WER (Word Error Rate):              {wer_score:.4f}  (lower is better)")
print(f"Top-1 Accuracy (Exact Match):       {top1_acc:.4f}  (higher is better)")
print(f"Mean Edit Distance:                 {mean_ed:.4f}  (lower is better)")
print(f"Normalized Edit Distance:           {norm_ed:.4f}  (lower is better)")
print(f"Precision (char-level):             {precision:.4f}  (higher is better)")
print(f"Recall (char-level):                {recall:.4f}  (higher is better)")
print(f"F1 Score (char-level):              {f1:.4f}  (higher is better)")
print(f"Partial Match (>=80% similarity):   {partial_match:.4f}  (higher is better)")