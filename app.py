from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

app = Flask(__name__)

# Initialize the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    """Speak out the given text."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Take voice command input from the microphone."""
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def run_alexa():
    """Run Alexa-like voice assistant."""
    command = take_command()
    print(f"Command received: {command}")
    response = ""

    if 'play' in command:
        song = command.replace('play', '')
        response = f'Playing {song}'
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        response = f'Current time is {time}'
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        response = info
    elif 'date' in command:
        response = 'Sorry, I have a headache'
    elif 'are you single' in command:
        response = 'I am in a relationship with WiFi'
    elif 'joke' in command:
        response = pyjokes.get_joke()
    else:
        response = 'Please say the command again.'

    # Speak the response
    talk(response)
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    """Flask route for the main page."""
    output = ""
    if request.method == "POST":
        if 'command' in request.form:
            # Execute the run_alexa function when user submits
            output = run_alexa()
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
