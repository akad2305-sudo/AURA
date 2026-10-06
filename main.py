import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import os
import datetime
import urllib.parse
import time


# =========================================================
# AURA SETTINGS
# =========================================================

ASSISTANT_NAME = "AURA"

recognizer = sr.Recognizer()

# ---------------------------------------------------------
# Text-to-Speech
# ---------------------------------------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

# Try to select a female Windows voice
voices = engine.getProperty("voices")

for voice in voices:
    voice_name = voice.name.lower()

    if (
        "zira" in voice_name
        or "female" in voice_name
        or "hazel" in voice_name
    ):
        engine.setProperty("voice", voice.id)
        break


# =========================================================
# SPEAK
# =========================================================

def speak(text):
    """Make AURA speak and print the same response."""

    if not text:
        return

    print(f"\n{ASSISTANT_NAME}: {text}")

    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)


# =========================================================
# MICROPHONE
# =========================================================

def listen():
    """Listen safely and convert speech to text."""

    with sr.Microphone() as source:

        print("\nListening...")

        try:
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.3
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except KeyboardInterrupt:
            print("\nVoice listening stopped.")
            return ""

        except Exception as e:
            print(f"Microphone error: {e}")
            return ""

    try:

        print("Understanding...")

        text = recognizer.recognize_google(audio)

        print(f"You: {text}")

        return text.lower().strip()

    except sr.UnknownValueError:

        print("AURA could not understand the speech.")

        speak("Sorry, I didn't understand that.")

        return ""

    except sr.RequestError as e:

        print("Speech recognition error:", e)

        speak(
            "I cannot connect to the speech recognition service right now."
        )

        return ""

    except Exception as e:

        print("Recognition error:", e)

        return ""


# =========================================================
# OPEN WEBSITE
# =========================================================

def open_website(url, name):

    speak(f"Opening {name}.")

    webbrowser.open(url)


# =========================================================
# YOUTUBE
# =========================================================

def youtube_search(command):

    query = command

    remove_words = [
        "open youtube",
        "youtube",
        "search youtube for",
        "search youtube",
        "play on youtube",
        "play",
        "video of",
        "video",
    ]

    for word in remove_words:
        query = query.replace(word, "")

    query = query.strip()

    if not query:
        speak("What would you like me to search for on YouTube?")
        return

    speak(f"Searching YouTube for {query}.")

    encoded_query = urllib.parse.quote_plus(query)

    url = (
        "https://www.youtube.com/results?search_query="
        + encoded_query
    )

    webbrowser.open(url)


# =========================================================
# SPOTIFY
# =========================================================

def spotify_search(command):

    query = command

    remove_words = [
        "open spotify",
        "spotify",
        "search spotify for",
        "search spotify",
        "play on spotify",
        "play",
        "song",
        "music",
    ]

    for word in remove_words:
        query = query.replace(word, "")

    query = query.strip()

    if not query:
        speak("What music would you like me to search for on Spotify?")
        return

    speak(f"Searching Spotify for {query}.")

    encoded_query = urllib.parse.quote_plus(query)

    url = (
        "https://open.spotify.com/search/"
        + encoded_query
    )

    webbrowser.open(url)


# =========================================================
# WINDOWS APPLICATIONS
# =========================================================

def open_windows_app(command):

    command = command.lower()

    # NOTEPAD
    if "notepad" in command:

        speak("Opening Notepad.")

        subprocess.Popen("notepad.exe")

        return True

    # CALCULATOR
    if "calculator" in command or "calc" in command:

        speak("Opening Calculator.")

        subprocess.Popen("calc.exe")

        return True

    # PAINT
    if "paint" in command:

        speak("Opening Paint.")

        subprocess.Popen("mspaint.exe")

        return True

    # FILE EXPLORER
    if (
        "file explorer" in command
        or "explorer" in command
        or "files" in command
    ):

        speak("Opening File Explorer.")

        subprocess.Popen("explorer.exe")

        return True

    # COMMAND PROMPT
    if "command prompt" in command or command == "cmd":

        speak("Opening Command Prompt.")

        subprocess.Popen("cmd.exe")

        return True

    # POWERSHELL
    if "powershell" in command:

        speak("Opening PowerShell.")

        subprocess.Popen("powershell.exe")

        return True

    # SETTINGS
    if "windows settings" in command or command == "settings":

        speak("Opening Windows Settings.")

        os.system("start ms-settings:")

        return True

    return False


# =========================================================
# SOCIAL / WEB SERVICES
# =========================================================

def open_service(command):

    command = command.lower()

    if "instagram" in command:

        open_website(
            "https://www.instagram.com",
            "Instagram"
        )

        return True

    if "whatsapp" in command:

        open_website(
            "https://web.whatsapp.com",
            "WhatsApp"
        )

        return True

    if "facebook" in command:

        open_website(
            "https://www.facebook.com",
            "Facebook"
        )

        return True

    if "gmail" in command:

        open_website(
            "https://mail.google.com",
            "Gmail"
        )

        return True

    if "google" in command:

        open_website(
            "https://www.google.com",
            "Google"
        )

        return True

    if "github" in command:

        open_website(
            "https://github.com",
            "GitHub"
        )

        return True

    if "youtube" in command:

        youtube_search(command)

        return True

    if "spotify" in command:

        spotify_search(command)

        return True

    return False


# =========================================================
# TIME / DATE
# =========================================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(f"The current time is {current_time}.")


def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(f"Today is {current_date}.")


# =========================================================
# SIMPLE SENTIMENT ANALYSIS
# =========================================================

def detect_sentiment(command):

    positive_words = [
        "happy",
        "great",
        "good",
        "awesome",
        "amazing",
        "excited",
        "love",
        "wonderful",
        "nice",
    ]

    negative_words = [
        "sad",
        "angry",
        "bad",
        "upset",
        "depressed",
        "hate",
        "terrible",
        "worried",
        "stressed",
        "frustrated",
    ]

    for word in positive_words:

        if word in command:

            return "positive"

    for word in negative_words:

        if word in command:

            return "negative"

    return "neutral"


def emotional_response(command):

    sentiment = detect_sentiment(command)

    if sentiment == "positive":

        speak(
            "I'm glad to hear that. "
            "That sounds great!"
        )

        return True

    if sentiment == "negative":

        speak(
            "I'm sorry you're feeling that way. "
            "I'm here with you. "
            "Tell me what happened and I'll try to help."
        )

        return True

    return False


# =========================================================
# GENERAL QUESTIONS
# =========================================================

def search_web(command):

    speak(
        "I don't have a built-in answer for that yet. "
        "I'll search the web for you."
    )

    encoded_query = urllib.parse.quote_plus(command)

    url = (
        "https://www.google.com/search?q="
        + encoded_query
    )

    webbrowser.open(url)


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(command):

    if not command:
        return True

    command = command.lower().strip()

    print(f"\nProcessing: {command}")

    # -----------------------------------------------------
    # EXIT
    # -----------------------------------------------------

    exit_commands = [
        "exit",
        "quit",
        "close aura",
        "shutdown aura",
        "goodbye",
        "bye",
    ]

    if command in exit_commands:

        speak("Goodbye. I'll be here when you need me.")

        return False

    # -----------------------------------------------------
    # STOP VOICE MODE
    # -----------------------------------------------------

    if (
        "stop listening" in command
        or "exit voice mode" in command
        or "stop voice mode" in command
    ):

        speak("Voice mode stopped.")

        return "voice_stop"

    # -----------------------------------------------------
    # GREETINGS
    # -----------------------------------------------------

    if command in [
        "hello",
        "hi",
        "hey",
        "hello aura",
        "hi aura",
        "hey aura",
    ]:

        speak(
            "Hello. I'm AURA. "
            "How can I help you?"
        )

        return True

    # -----------------------------------------------------
    # WHO ARE YOU
    # -----------------------------------------------------

    if (
        "who are you" in command
        or "what are you" in command
    ):

        speak(
            "I am AURA, your personal desktop voice assistant."
        )

        return True

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if "what time" in command or "current time" in command:

        tell_time()

        return True

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    if (
        "what date" in command
        or "today's date" in command
        or "what day is it" in command
    ):

        tell_date()

        return True

    # -----------------------------------------------------
    # YOUTUBE
    # -----------------------------------------------------

    if "youtube" in command:

        youtube_search(command)

        return True

    # -----------------------------------------------------
    # SPOTIFY
    # -----------------------------------------------------

    if "spotify" in command:

        spotify_search(command)

        return True

    # -----------------------------------------------------
    # WINDOWS APPLICATIONS
    # -----------------------------------------------------

    if open_windows_app(command):

        return True

    # -----------------------------------------------------
    # WEBSITES / SERVICES
    # -----------------------------------------------------

    if open_service(command):

        return True

    # -----------------------------------------------------
    # SENTIMENT
    # -----------------------------------------------------

    if emotional_response(command):

        return True

    # -----------------------------------------------------
    # COMMON QUESTIONS
    # -----------------------------------------------------

    if (
        "what is" in command
        or "who is" in command
        or "where is" in command
        or "when is" in command
        or "how to" in command
        or "tell me about" in command
        or "explain" in command
    ):

        search_web(command)

        return True

    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    speak(
        "I can help with that, but I don't have "
        "that feature built in yet. "
        "I'll search the web for you."
    )

    search_web(command)

    return True


# =========================================================
# TYPING MODE
# =========================================================

def typing_mode():

    speak(
        "Typing mode is ready. "
        "Type your command whenever you're ready."
    )

    while True:

        try:

            command = input("\nYou: ").strip()

        except KeyboardInterrupt:

            print("\n")

            speak("Typing mode stopped.")

            return True

        if not command:
            continue

        result = process_command(command)

        if result is False:

            return False

        if result == "voice_stop":

            speak(
                "You're already in typing mode."
            )


# =========================================================
# VOICE MODE
# =========================================================

def voice_mode():

    speak(
        "Voice mode is ready. "
        "I'm listening."
    )

    while True:

        command = listen()

        if not command:

            continue

        result = process_command(command)

        if result is False:

            return False

        if result == "voice_stop":

            speak(
                "Returning to the main menu."
            )

            return True


# =========================================================
# MAIN MENU
# =========================================================

def main():

    speak(
        "Hello. I am AURA, your personal assistant."
    )

    while True:

        print("\n")
        print("=" * 45)
        print("                 AURA")
        print("=" * 45)
        print("1. 🎤 Voice mode")
        print("2. ⌨️  Typing mode")
        print("3. ❌ Exit")
        print("=" * 45)

        try:

            choice = input("Choose: ").strip()

        except KeyboardInterrupt:

            print("\n")

            speak("Goodbye.")

            break

        # -------------------------------------------------
        # VOICE
        # -------------------------------------------------

        if choice == "1":

            result = voice_mode()

            if result is False:

                break

        # -------------------------------------------------
        # TYPING
        # -------------------------------------------------

        elif choice == "2":

            result = typing_mode()

            if result is False:

                break

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        elif choice == "3":

            speak(
                "Goodbye. Have a great day."
            )

            break

        # -------------------------------------------------
        # INVALID
        # -------------------------------------------------

        else:

            speak(
                "Please choose 1 for voice mode, "
                "2 for typing mode, or 3 to exit."
            )


# =========================================================
# START AURA
# =========================================================

if __name__ == "__main__":

    main()