from flask import Flask, request, jsonify, render_template_string
import webbrowser

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: #080b12;
            color: white;
            font-family: Arial, sans-serif;
        }

        .container {
            width: 100%;
            max-width: 500px;
            margin: auto;
            padding: 25px 20px;
        }

        .header {
            text-align: center;
        }

        .orb {
            width: 110px;
            height: 110px;
            margin: 20px auto;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                white 0%,
                #65c7ff 20%,
                #1677ff 45%,
                #071c46 75%
            );

            box-shadow:
                0 0 20px #168cff,
                0 0 50px #126cff;

            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.08);
            }
        }

        h1 {
            font-size: 32px;
            margin: 10px;
        }

        .status {
            color: #65c7ff;
            margin-bottom: 20px;
        }

        .chat {
            background: #101520;
            border-radius: 20px;
            padding: 15px;
            min-height: 300px;
            max-height: 50vh;
            overflow-y: auto;
        }

        .message {
            padding: 12px 15px;
            border-radius: 15px;
            margin: 10px 0;
            max-width: 85%;
        }

        .user {
            background: #1769aa;
            margin-left: auto;
        }

        .aura {
            background: #252c38;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: #1b2230;
            color: white;
            font-size: 16px;
            outline: none;
        }

        button {
            border: none;
            border-radius: 15px;
            padding: 15px;
            background: #147cff;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        .mic {
            width: 100%;
            margin-top: 10px;
            background: #202938;
        }

        .quick {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }

        .quick button {
            background: #151d2b;
        }
    </style>
</head>

<body>

<div class="container">

    <div class="header">

        <div class="orb"></div>

        <h1>AURA</h1>

        <div class="status" id="status">
            Online
        </div>

    </div>

    <div class="chat" id="chat">

        <div class="message aura">
            Hello, I am AURA. Your personal assistant.
        </div>

    </div>

    <div class="controls">

        <input
            id="command"
            placeholder="Type a command..."
            onkeydown="if(event.key === 'Enter') sendCommand()"
        >

        <button onclick="sendCommand()">
            Send
        </button>

    </div>

    <button class="mic" onclick="startListening()">
        🎤 Speak to AURA
    </button>

    <div class="quick">

        <button onclick="quickCommand('open YouTube')">
            ▶ YouTube
        </button>

        <button onclick="quickCommand('open Spotify')">
            🎵 Spotify
        </button>

        <button onclick="quickCommand('open WhatsApp')">
            💬 WhatsApp
        </button>

        <button onclick="quickCommand('open Instagram')">
            📷 Instagram
        </button>

    </div>

</div>

<script>

function addMessage(text, type) {

    const chat = document.getElementById("chat");

    const message = document.createElement("div");

    message.className = "message " + type;

    message.innerText = text;

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


async function sendCommand() {

    const input = document.getElementById("command");

    const command = input.value.trim();

    if (!command) {
        return;
    }

    addMessage(command, "user");

    input.value = "";

    document.getElementById("status").innerText =
        "Thinking...";

    try {

        const response = await fetch("/command", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                command: command
            })

        });

        const data = await response.json();

        addMessage(data.response, "aura");

        document.getElementById("status").innerText =
            "Online";

        speak(data.response);

    } catch (error) {

        addMessage(
            "Could not connect to AURA.",
            "aura"
        );

        document.getElementById("status").innerText =
            "Connection error";
    }
}


function quickCommand(command) {

    document.getElementById("command").value =
        command;

    sendCommand();
}


function speak(text) {

    if ("speechSynthesis" in window) {

        const speech =
            new SpeechSynthesisUtterance(text);

        speech.rate = 1;

        speech.pitch = 1;

        window.speechSynthesis.speak(speech);
    }
}


function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        addMessage(
            "Voice recognition is not supported. Try Chrome.",
            "aura"
        );

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    document.getElementById("status").innerText =
        "Listening...";

    recognition.start();

    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;

        document.getElementById("command").value =
            text;

        sendCommand();
    };

    recognition.onerror = function() {

        document.getElementById("status").innerText =
            "Voice error";
    };

    recognition.onend = function() {

        document.getElementById("status").innerText =
            "Online";
    };
}

</script>

</body>
</html>
"""


def execute_command(command):

    command_lower = command.lower().strip()

    if "open youtube" in command_lower:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "Opening YouTube."


    if "open spotify" in command_lower:

        webbrowser.open(
            "https://open.spotify.com"
        )

        return "Opening Spotify."


    if "open whatsapp" in command_lower:

        webbrowser.open(
            "https://web.whatsapp.com"
        )

        return "Opening WhatsApp."


    if "open instagram" in command_lower:

        webbrowser.open(
            "https://www.instagram.com"
        )

        return "Opening Instagram."


    if "open google" in command_lower:

        webbrowser.open(
            "https://www.google.com"
        )

        return "Opening Google."


    if "open gmail" in command_lower:

        webbrowser.open(
            "https://mail.google.com"
        )

        return "Opening Gmail."


    return (
        "I received your command: "
        + command
    )


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()

    if not data:

        return jsonify({
            "response": "No command received."
        })


    user_command = data.get(
        "command",
        ""
    )


    if not user_command:

        return jsonify({
            "response": "Please enter a command."
        })


    response = execute_command(
        user_command
    )


    return jsonify({
        "response": response
    })


if __name__ == "__main__":

    print("=" * 50)
    print("AURA MOBILE SERVER")
    print("=" * 50)

    print()
    print("AURA is starting...")
    print()
    print("Computer address:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )