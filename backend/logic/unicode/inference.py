from keras.models import Model, load_model
from keras.layers import Input
import numpy as np

# Define constants
num_encoder_tokens = 63
num_decoder_tokens = 28
max_input_len = 19
max_target_len = 31
input_char_index = {'ँ': 0, 'ं': 1, 'ः': 2, 'अ': 3, 'आ': 4, 'इ': 5, 'ई': 6, 'उ': 7, 'ऊ': 8, 'ऋ': 9, 'ए': 10, 'ऐ': 11, 'ऑ': 12, 'ओ': 13, 'औ': 14, 'क': 15, 'ख': 16, 'ग': 17, 'घ': 18, 'ङ': 19, 'च': 20, 'छ': 21, 'ज': 22, 'झ': 23, 'ञ': 24, 'ट': 25, 'ठ': 26, 'ड': 27, 'ढ': 28, 'ण': 29, 'त': 30, 'थ': 31, 'द': 32, 'ध': 33, 'न': 34, 'प': 35, 'फ': 36, 'ब': 37, 'भ': 38, 'म': 39, 'य': 40, 'र': 41, 'ल': 42, 'व': 43, 'श': 44, 'ष': 45, 'स': 46, 'ह': 47, '़': 48, 'ऽ': 49, 'ा': 50, 'ि': 51, 'ी': 52, 'ु': 53, 'ू': 54, 'ृ': 55, 'े': 56, 'ै': 57, 'ॉ': 58, 'ो': 59, 'ौ': 60, '्': 61, '॰': 62}
target_char_index = {'$': 0, '^': 1, 'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9, 'i': 10, 'j': 11, 'k': 12, 'l': 13, 'm': 14, 'n': 15, 'o': 16, 'p': 17, 'q': 18, 'r': 19, 's': 20, 't': 21, 'u': 22, 'v': 23, 'w': 24, 'x': 25, 'y': 26, 'z': 27}

target_chars = list(target_char_index.keys())

# Load the trained model
model = load_model('logic/unicode/models/model_130.h5')

# Extract encoder and decoder models
encoder_inputs = model.input[0]
encoder_outputs, state_h_enc, state_c_enc = model.get_layer('lstm').output
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

decoder_inputs = model.input[1]
decoder_lstm = model.get_layer('lstm_1')
decoder_dense = model.get_layer('dense')

decoder_state_input_h = Input(shape=(256,), name="decoder_state_input_h")
decoder_state_input_c = Input(shape=(256,), name="decoder_state_input_c")
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)


# Decode sequence function remains the same
def decode_sequence(input_seq):
    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, target_char_index['^']] = 1.0
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = target_chars[sampled_token_index]
        decoded_sentence += sampled_char
        if (sampled_char == '$' or len(decoded_sentence) > max_target_len):
            stop_condition = True
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.0
        states_value = [h, c]
    return decoded_sentence

# Predict output function remains the same
# def predict_output(input_text):
#     words = input_text.split(' ')
#     transliterated_words = []
#     for word in words:
#         input_seq = np.zeros((1, max_input_len, num_encoder_tokens), dtype='float32')
#         for t, char in enumerate(word):
#             input_seq[0, t, input_char_index[char]] = 1
#         decoded_word = decode_sequence(input_seq)
#         transliterated_words.append(decoded_word.rstrip('$'))
#     return ' '.join(transliterated_words)




def predict_output(input_text):
    # Step 1: Split input text into words
    words = input_text.split(' ')
    
    # Step 2: Process each word
    transliterated_words = []
    for word in words:
        # Detect and remove special characters
        replacement = ''
        if ',' in word:
            word = word.replace(',', '')
            replacement = ','
        elif '।' in word:
            word = word.replace('।', '')
            replacement = '.'
        
        # Prepare the cleaned word for the model
        input_seq = np.zeros((1, max_input_len, num_encoder_tokens), dtype='float32')
        for t, char in enumerate(word):
            input_seq[0, t, input_char_index.get(char, 0)] = 1  # Use 0 if char is not in input_char_index
        
        # Get the transliterated word
        decoded_word = decode_sequence(input_seq)
        transliterated_word = decoded_word.rstrip('$')  # Remove end token if present
        
        # Add the replacement character back (comma or period)
        transliterated_words.append(transliterated_word + replacement)
    
    # Step 3: Recombine words with replacements into a final sentence
    final_sentence = ' '.join(transliterated_words)
    return final_sentence




# Test the prediction
# text = 'मेरो नाम निका महर्जन हो'
# print('Nepali text:', text)
# print('Transliterated English text:', predict_output(text))
