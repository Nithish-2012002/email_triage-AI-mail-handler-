import speech_recognition as sr

def transcribe_audio(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

# Example usage
transcribed_text = transcribe_audio('harvard.wav')
print(f"Transcribed Text:\n{transcribed_text}")