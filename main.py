import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pyjokes
import wikipedia
from datetime import datetime

newsapi = "0c85e636ce6f4fd28d758b1a169596d2"

def speak(text):
    engine = pyttsx3.init('sapi5')  # Force Windows SAPI5 voice engine
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Try voices[1] if needed
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")

    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram")

    elif "open github" in c:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")

    elif "news" in c:
        speak("Fetching latest news from India")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])[:5]
                for article in articles:
                    title = article.get('title')
                    if title:
                        speak(title)
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            speak("There was an error fetching the news.")
            print(e)

    elif "time" in c:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "joke" in c:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "who are you" in c or ("who" in c and "you" in c):
        speak("I am Jarvis, your virtual assistant.")

    elif "who made you" in c or "who created you" in c:
        speak("I was developed by Salman. His GitHub is numaan28.")

    elif "who is" in c or "what is" in c or "tell me about" in c or "when did" in c:
        speak("Let me search that for you...")
        try:
            query = c.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("Your query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any result for that.")
        except Exception as e:
            speak("Something went wrong while searching.")
            print(e)

    elif "exit" in c or "quit" in c:
        speak("Goodbye!")
        exit()

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for activation word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                word = recognizer.recognize_google(audio).lower()

                if "jarvis" in word:
                    speak("Yes sir, I'm here.")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        print("Waiting for command...")
                        audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(audio)
                        processcommand(command)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("Didn't understand. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
