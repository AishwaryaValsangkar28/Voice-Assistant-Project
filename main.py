import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import webbrowser
import subprocess
import time
import datetime
import requests
import wikipedia
import whisper
import ecapture as ec
from loguru import logger

logger.info(f'Loading your personal voice assistant')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hey, Good Morning")
        print("Hey, Good Morning")

    elif 12 <= hour < 18:
        speak("Hey, Good Afternoon")
        logger.info("Hey, Good Afternoon")

    else:
        speak("Hey, Good Evening")
        logger.info("Hey, Good Evening")


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            a = recognizer.recognize_google(audio)
            logger.debug(f"User said: {a}\n")
            return a.lower()

        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return 'none'

        except sr.RequestError as e:
            logger.error(f"Speech recognition request failed: {e}")
            speak("Sorry, there was an error with speech recognition. Please try again.")
            return 'none'

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            speak("Sorry, there was an error. Please try again.")
            return 'none'


speak("Loading your Personal Assistant Siri")
wish_me()


if __name__ == '__main__':
    while True:
        speak("How can I help you today?")
        statement = take_command()

        if statement == 'none':
            continue

        if any(keyword in statement for keyword in ["good bye", "ok bye", "stop"]):
            speak("Your Personal Assistant is shutting down, Good Bye")
            logger.info("Your Personal Assistant is shutting down, Good Bye")
            break

        if "wikipedia" in statement:
            speak("Searching Wikipedia...")
            statement = statement.replace("wikipedia", "")
            result = wikipedia.summary(statement, sentences=10)
            speak("According to wikipedia")
            speak(result)
            logger.info(result)

        elif "open youtube" in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is open now")
            time.sleep(10)

        elif "open google" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is open now")
            time.sleep(10)

        elif "open gmail" in statement:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Google mail is open now")
            time.sleep(10)

        elif "weather" in statement:
            API_KEY = 'f0817b502a13e8c484e89903bf0d40d7'
            base_url = "http://maps.openweathermap.org/maps/2.0/weather?"
            speak("What is the name of your city?")
            city_name = take_command()
            complete_url = base_url + "appid=" + API_KEY + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x['cod'] != '404':
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak("Temperature in Kelvin is "
                      + str(current_temperature)
                      + "\n Humidity in percentage is" + str(current_humidity)
                      + "\n description " + str(weather_description))
                logger.info(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidity) +
                      "\n description = " +
                      str(weather_description))

            else:
                logger.error("City not found")

        elif "time" in statement:
            Time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is{Time}")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Stackoverflow is open now, Please login!")

        elif "news" in statement:
            webbrowser.open_new_tab("https://www.wionews.com/live-tv")
            speak("Here are some latest news.")

        elif "camera" in statement or "take a picture" in statement:
            ec.capture(0, 'test', 'img.jpg')

        # The video will we recorded for 10 seconds.
        elif "video" in statement:
            ec.vidCapture(0, "test", "video.avi", 10)

        elif "log off" in statement:
            speak("Ok, Your PC will log off in 10 sec")
            subprocess.call(["shutdown", "/l"])

time.sleep(5)
