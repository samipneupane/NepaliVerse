import librosa
import numpy as np
import noisereduce as nr
# from python_speech_features import mfcc
import speech_recognition as sr
import librosa.display
import re
from fuzzywuzzy import fuzz
# from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from jiwer import wer
import difflib


def reduce_noise(audio_path, noise_duration=0.5, noise_reduction_method="noisereduce"):
    audio, sr = librosa.load(audio_path, sr=None)

    if noise_reduction_method == "noisereduce":
        noise_sample = audio[:int(noise_duration * sr)]
        reduced_noise_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_sample)
    #elif noise_reduction_method == "spectral_gating":
    #    pass
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

    if text is None:  # Handle None values
        return ""

    # Remove punctuation and special characters
    text = re.sub(r'[^\u0900-\u097F\s]', '', text)

    # Remove white spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def compare_speech_similarity(user_audio_path, reference_audio_path):
    # Load user audio
    user_audio, sr_user = reduce_noise(user_audio_path)

    # Load reference audio
    # user_audio, sr_user = librosa.load(user_audio_path, sr=None)
    reference_audio, sr_reference = librosa.load(reference_audio_path, sr=None)

    # Resample both audios to 16000 Hz
    user_audio = librosa.resample(user_audio, orig_sr=sr_user, target_sr=16000)
    reference_audio = librosa.resample(reference_audio, orig_sr=sr_reference, target_sr=16000)

    # Update sample rates after resampling
    sr_user = 16000
    sr_reference = 16000

    # Trim Silence
    user_audio, _ = librosa.effects.trim(user_audio, top_db=20)
    reference_audio, _ = librosa.effects.trim(reference_audio, top_db=20)

    # Get the transcription of user and reference audio using Speech Recognition
    user_transcription = recognize_speech(user_audio_path)
    reference_transcription = recognize_speech(reference_audio_path)

    #Print transcriptions to verify Speech-to-Text
    # print(f"User Transcription: {user_transcription}")
    # print(f"Reference Transcription: {reference_transcription}")

    # Preprocess transcriptions
    user_transcription = preprocess_text(user_transcription)
    reference_transcription = preprocess_text(reference_transcription)

    # Calculate fuzzy similarity score
    similarity_score = fuzz.ratio(user_transcription, reference_transcription)
    # print(f"Fuzzy Similarity Score: {similarity_score}")

    # Compare transcriptions using a similarity threshold
    if similarity_score >= 90:
        similarity_category = "Similar"
        mispronounced_words = []  # No mispronounced words if similar
    elif similarity_score >= 70:
        similarity_category = "Partially Similar"
        error = wer(reference_transcription, user_transcription)
        # print(f"Word Error Rate (WER): {error}")
        diff = difflib.ndiff(reference_transcription.split(), user_transcription.split())
        mispronounced_words = [word[2:] for word in diff if word.startswith('+ ')]
    else:
        similarity_category = "Not Similar"
        error = wer(reference_transcription, user_transcription)
        # print(f"Word Error Rate (WER): {error}")
        diff = difflib.ndiff(reference_transcription.split(), user_transcription.split())
        mispronounced_words = [word[2:] for word in diff if word.startswith('+ ')]

    # print(f"Similarity Category: {similarity_category}")
    # print(f"Potentially Mispronounced Words: {mispronounced_words}")

    return similarity_category , similarity_score


# user_audio_path = 'Voice8.wav'  # Replace with your user audio file path
# reference_audio_path = '333f497c030f44978009a444d75601a8.wav'  # Replace with your reference audio file path

# compare_speech_similarity(user_audio_path, reference_audio_path)