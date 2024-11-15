# Define mappings for Nepali script and diacritics
nepali = {
    'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'u': 'उ', 'uu': 'ऊ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',
    'k': 'क्', 'ka': 'क', 'kh': 'ख्', 'kha': 'ख', 'g': 'ग्', 'ga': 'ग', 'gh': 'घ्', 'gha': 'घ',
    'ch': 'च्', 'cha': 'च', 'chh': 'छ्', 'chha': 'छ', 'j': 'ज्', 'ja': 'ज', 'jh': 'झ्', 'jha': 'झ',
    't': 'त्', 'ta': 'त', 'th': 'थ्', 'tha': 'थ', 'T': 'ट्', 'Ta': 'ट', 'Th': 'ठ्', 'Tha': 'ठ',
    'd': 'द्', 'da': 'द', 'D': 'ड्', 'Da': 'ड', 'Dh': 'ढ्', 'Dha': 'ढ', 'dh': 'ध्', 'dha': 'ध',
    'n': 'न्', 'na': 'न', 'Ng': 'ङ्', 'Nga': 'ङ', 'N': 'ण्', 'Na': 'ण', 'Yn': 'ञ्', 'Y': 'य्', 'Ya': 'य', 'Yna': 'ञ',
    'p': 'प्', 'pa': 'प', 'ph': 'फ्', 'pha': 'फ', 'b': 'ब्', 'ba': 'ब', 'bh': 'भ्', 'bha': 'भ',
    'm': 'म्', 'ma': 'म', 'y': 'य्', 'ya': 'य', 'r': 'र्', 'ra': 'र', 'rr': 'र्',
    'l': 'ल्', 'la': 'ल', 'v': 'व्', 'va': 'व', 'sh': 'श्', 'sha': 'श', 's': 'स्', 'sa': 'स',
    'shh': 'ष्', 'shha': 'ष', 'h': 'ह्', 'ha': 'ह', 'f': 'फ्', 'fa': 'फ',
    'w': 'व्', 'wa': 'व', 'x': 'ज्', 'xa': 'ज', 'z': 'ज्', 'za': 'ज', 'O': 'ॐ'
}

# Define diacritics for vowel sounds that follow a consonant+halanta sequence
shabda_banot = {
    'a': '',  # inherent vowel, so we remove halanta
    'aa': 'ा', 'i': 'ि', 'ii': 'ी', 'u': 'ु', 'uu': 'ू', 'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ'
}

def separate_letters(word):
    """Separate Nepali word into individual characters"""
    return [char for char in word]

def create_reverse_mapping():
    """Create reverse mappings for both nepali and shabda_banot dictionaries"""
    reverse_nepali = {}
    for eng, nep in nepali.items():
        if eng.endswith('a') and len(eng) > 1:
            base_consonant = eng[:-1]
            reverse_nepali[nep] = base_consonant
        else:
            reverse_nepali[nep] = eng
    
    reverse_shabda = {nep: eng for eng, nep in shabda_banot.items() if nep}
    return reverse_nepali, reverse_shabda

def translate_nepali_to_english(word):
    """Translate a Nepali word to its English phonetic equivalent"""
    reverse_nepali, reverse_shabda = create_reverse_mapping()
    result = []
    i = 0
    
    while i < len(word):
        char = word[i]
        
        # Check for vowel diacritics following a consonant
        if i < len(word) - 1 and word[i + 1] in reverse_shabda:
            base_consonant = reverse_nepali.get(char + '्', reverse_nepali.get(char, char))
            diacritic = reverse_shabda[word[i + 1]]
            result.append(base_consonant + diacritic)
            i += 2
            continue

        # If the next character is a halanta, treat the pair as a conjunct (like न् + consonant)
        elif i < len(word) - 1 and word[i + 1] == '्':
            result.append(reverse_nepali.get(char + '्', reverse_nepali.get(char, char)))
            i += 2
            continue
        
        # For standalone consonants, default to adding 'a' (inherent vowel)
        elif char in reverse_nepali:
            eng_char = reverse_nepali[char]
            if eng_char and eng_char[-1] != 'a':
                result.append(eng_char + 'a')
            else:
                result.append(eng_char)
        
        elif char in reverse_shabda:
            result.append(reverse_shabda[char])
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)

# Get user input
user_input = input("Enter a Nepali word or sentence: ")

# Process the user input
separated = separate_letters(user_input)
english = translate_nepali_to_english(user_input)

# print("\nNepali Word Analysis:")
# print("-" * 50)
# print(f"Original: {user_input}")
# print(f"Separated: {' + '.join(separated)}")
print(f"{english}")
