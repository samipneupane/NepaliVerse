import editdistance

def calculate_cer(actual_file, predicted_file):
    with open(actual_file, 'r', encoding='utf-8') as actual_f, open(predicted_file, 'r', encoding='utf-8') as predicted_f:
        actual_lines = actual_f.readlines()
        predicted_lines = predicted_f.readlines()
        
        if len(actual_lines) != len(predicted_lines):
            raise ValueError("The two files must have the same number of lines.")
        
        total_characters = 0
        total_errors = 0
        
        # Iterate over each line in both files
        for actual_line, predicted_line in zip(actual_lines, predicted_lines):
            actual_line = actual_line.strip()
            predicted_line = predicted_line.strip()
            
            edit_dist = editdistance.eval(actual_line, predicted_line)
            
            total_errors += edit_dist
            total_characters += len(actual_line)
        
        cer = total_errors / total_characters if total_characters > 0 else 0
        
        return cer

# Example usage:
actual_file = 'logic/unicode/actual_predicted/actual_all.txt'
predicted_file = 'logic/unicode/actual_predicted/predicted_all.txt'

cer = calculate_cer(actual_file, predicted_file)
print(f"Character Error Rate (CER): {cer:.4f}")
