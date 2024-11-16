import librosa
import noisereduce as nr
import speech_recognition as sr
import librosa.display
import re
from fuzzywuzzy import fuzz
from jiwer import wer
import difflib


def reduce_noise(audio_path, noise_duration=0.5, noise_reduction_method="noisereduce"):
    audio, sr = librosa.load(audio_path, sr=None)

    if noise_reduction_method == "noisereduce":
        noise_sample = audio[:int(noise_duration * sr)]
        reduced_noise_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_sample)

    else:
        reduced_noise_audio = audio

    # Normalize intensity
    reduced_noise_audio = librosa.util.normalize(reduced_noise_audio)

    return reduced_noise_audio, sr


def recognize_speech(audio_path):

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="ne-IN")  # Nepali language
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    

def preprocess_text(text):
    if text is None:
        return ""

    text = re.sub(r'[^\u0900-\u097F\s]|।', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def compare_speech_similarity(user_audio_path, reference_transcription):
    
    user_audio, sr_user = reduce_noise(user_audio_path)

    # Resample audio to 16000 Hz
    user_audio = librosa.resample(user_audio, orig_sr=sr_user, target_sr=16000)

    # Update sample rates after resampling
    sr_user = 16000

    # Trim Silence
    user_audio, _ = librosa.effects.trim(user_audio, top_db=20)

    # Get the transcription of user and reference audio using Speech Recognition
    user_transcription = recognize_speech(user_audio_path)

    # Preprocess transcriptions
    user_transcription = preprocess_text(user_transcription)
    reference_transcription = preprocess_text(reference_transcription)

    # Calculate fuzzy similarity score
    similarity_score = fuzz.ratio(user_transcription, reference_transcription)

    error = None
    if similarity_score >= 90:
        similarity_category = "Similar"
        mispronounced_words = []
    elif similarity_score >= 70:
        similarity_category = "Partially Similar"
        error = wer(reference_transcription, user_transcription)
        diff = difflib.ndiff(user_transcription.split(), reference_transcription.split())
        mispronounced_words = [word[2:] for word in diff if word.startswith('+ ')]
    else:
        similarity_category = "Not Similar"
        error = wer(reference_transcription, user_transcription)
        diff = difflib.ndiff(user_transcription.split(), reference_transcription.split())
        mispronounced_words = [word[2:] for word in diff if word.startswith('+ ')]

    # print(f"User Transcription: {user_transcription}")
    # print(f"Reference Transcription: {reference_transcription}")
    # print(f"Similarity Score: {similarity_score}")
    # print(f"Similarity Category: {similarity_category}")
    # print(f"Potentially Mispronounced Words: {mispronounced_words}")
    # print(f"Word Error Rate (WER): {error}")

    # with open("output.txt", "w", encoding="utf-8") as file:
    #     file.write(f"User Transcription: {user_transcription}\n")
    #     file.write(f"Reference Transcription: {reference_transcription}\n")
    #     file.write(f"Similarity Score: {similarity_score}\n")
    #     file.write(f"Similarity Category: {similarity_category}\n")
    #     file.write(f"Potentially Mispronounced Words: {', '.join(mispronounced_words)}\n")
    #     file.write(f"Word Error Rate (WER): {error}\n")

    return {
        "similarity_score": similarity_score, 
        "similarity_category": similarity_category,
        "mispronounced_words": mispronounced_words,
        "word_error_rate": error}


# user_audio_path = 'logic/similarity/audiofiles/desh_00.wav'
# reference_text = 'मलाई मेरो देश प्यारो लाग्छ'

# compare_speech_similarity(user_audio_path, reference_text)
