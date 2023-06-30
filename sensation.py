import os
import speech_recognition as sr
import pyttsx3
import datetime
import threading
import geocoder

def listen_and_recognize():
    r = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    sensation_active = False

    # Initial welcome message
    print("Welcome to Sensation")
    text_to_speech(engine, "Welcome to Sensation. You can start speaking now.")

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
                result = r.recognize_google(audio)
                print("You spoke:", result)
                text_to_speech(engine, "You said: " + result)

                if result.lower() == "start sensation":
                    if not sensation_active:
                        sensation_active = True
                        print("Sensation started.")
                        text_to_speech(engine, "Sensation started.")
                elif result.lower() == "stop sensation":
                    if sensation_active:
                        sensation_active = False
                        print("Sensation stopped.")
                        text_to_speech(engine, "Sensation stopped.")
                elif sensation_active:
                    if "what" in result.lower() and "time" in result.lower():
                        current_time = datetime.datetime.now().strftime("%H:%M")
                        print("The current time is:", current_time)
                        text_to_speech(engine, "The current time is " + current_time)
                    elif "position" in result.lower() or "location" in result.lower():
                        position = get_current_position()
                        print("Current position:", position)
                        text_to_speech(engine, "Your current position is " + position)
                    elif "picture" in result.lower() or "photo" in result.lower():
                        # take_picture()
                        print("Picture was successfully stored.")
                        text_to_speech(engine, "Picture was successfully stored.")
                    elif "say hi to" in result.lower():
                        name = result.lower().split("say hi to")[1].strip()
                        print("Hello", name)
                        text_to_speech(engine, "Hello " + name)
                    elif result.lower() == "shut down sensation":
                        print("Shutting down Sensation...")
                        text_to_speech(engine, "Shutting down Sensation.")
                        break
                    else:
                        text_to_speech(engine, "Invalid command.")
                else:
                    if result.lower() == "shut down sensation":
                        print("Shutting down Sensation...")
                        text_to_speech(engine, "Shutting down Sensation.")
                        break
                    else:
                        print("Sensation is not active. Start Sensation to proceed.")
                        text_to_speech(engine, "Sensation is not active. Start Sensation to proceed.")

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Error:", e)

def text_to_speech(engine, text):
    engine.say(text)
    engine.runAndWait()

# Function to retrieve the current position
def get_current_position():
    g = geocoder.ip('me')
    if g.ok:
        city = g.city if g.city else ""
        state = g.state if g.state else ""
        country = g.country if g.country else ""
        street = g.street if g.street else ""
        return f"{street}, {city}, {state}"
    else:
        return "Unable to retrieve current position"

# Call the listen_and_recognize() function
listen_and_recognize()
