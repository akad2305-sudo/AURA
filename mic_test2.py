import speech_recognition as sr

r = sr.Recognizer()

print("==============================")
print("JARVIS MICROPHONE TEST 2")
print("==============================")

with sr.Microphone(device_index=1) as source:
    print("Microphone opened!")
    print("Speak now: Hello Jarvis")
    audio = r.listen(source, timeout=5, phrase_time_limit=5)

print("Audio captured!")
print("Audio size:", len(audio.frame_data), "bytes")
print("Recognizing...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Google could not understand your voice.")
except sr.RequestError as e:
    print("Google connection error:", e)