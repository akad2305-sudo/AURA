import speech_recognition as sr

r = sr.Recognizer()

print("================================")
print("JARVIS MICROPHONE TEST")
print("================================")

with sr.Microphone(device_index=1) as source:
    print("Microphone opened!")
    print("Adjusting for background noise...")
    r.adjust_for_ambient_noise(source, duration=1)

    print()
    print("SPEAK NOW!")
    print("Say: HELLO JARVIS")
    print("You have 5 seconds...")

    audio = r.listen(source, timeout=5, phrase_time_limit=5)

print()
print("Recording finished!")
print("Audio size:", len(audio.frame_data), "bytes")
print()
print("Sending audio to Google...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)

except sr.UnknownValueError:
    print("Google could not understand your voice.")

except sr.RequestError as e:
    print("Google connection error:", e)