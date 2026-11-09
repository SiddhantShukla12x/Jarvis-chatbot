import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests


newsapiKey = "7a58a3d25a7042fb933f3b556090a7a5"

def speak(text):  
    engine = pyttsx3.init() 
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapiKey}")
        if response.status_code == 200:
            data = response.json()
            articles = data["articles"]
            
            news_text = "Here are the top news headlines. "
            for i, article in enumerate(articles[:5], start=1):
             news_text += f"{i}. {article['title']}. "
        
            print(news_text)  
            speak(news_text)  
        else:
            speak("Could not fetch news right now.")

if __name__ == "__main__":
    speak("Initializing Jarvis")   

    while True:
        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=4, phrase_time_limit=4)

            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                print("Jarvis Active...")
                speak("Yes sir")

                try:
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)

                    command = r.recognize_google(audio, language='en-IN')
                    print(f"Command: {command}")
                    processCommand(command)

                except sr.UnknownValueError:
                    print("Could not understand command")
                except Exception as e:
                    print("Error: ", e)
                    
        except Exception as e:
            print("Error:", e)
      