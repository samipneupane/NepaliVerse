import librosa
import noisereduce as nr
import speech_recognition as sr
import re
from fuzzywuzzy import fuzz
from jiwer import wer
import difflib
from io import BytesIO
from pydub import AudioSegment


recognizer = sr.Recognizer()


def recognize_speech(audio_data):
    try:
        # Convert the audio to PCM WAV in-memory
        audio_segment = AudioSegment.from_file(audio_data)
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1) 
        wav_io = BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Use BytesIO object as the audio source
        with sr.AudioFile(wav_io) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)

        # Recognize speech using Google's speech recognition
        text = recognizer.recognize_google(audio, language="ne-IN")  # Nepali language
        # print(f"Recognized text: {text}")
        return text

    except sr.UnknownValueError:
        # print("Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        # print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        # print(f"An error occurred: {e}")
        return None

    

def preprocess_text(text):
    if text is None:
        return ""

    text = re.sub(r'[^\u0900-\u097F\s]|।', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def compare_speech_similarity(audio_data, reference_transcription):

    # Get the transcription of user and reference audio using Speech Recognition
    user_transcription = recognize_speech(audio_data)

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
