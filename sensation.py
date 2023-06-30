import os
import speech_recognition as sr
import pyttsx3
import datetime
import threading

def listen_and_recognize():
    r = sr.Recognizer()
    engine = pyttsx3.init()  # Initialize the pyttsx3 engine once
    engine.setProperty("rate", 150)  # Set the speech rate to 150 words per minute

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        navigation_started = False  # Flag to track navigation start

        print("Start Speaking")
        while True:
            try:
                audio = r.listen(source, timeout=0.5)  # Set a timeout for listening
                result = r.recognize_google(audio)  # Use Google Web Speech API for speech recognition
                print("You spoke: " + result)

                if "what" in result.lower() and "time" in result.lower():
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    print("The current time is:", current_time)
                    text_to_speech(engine, "The current time is " + current_time)
                elif result.lower() == "start navigation":
                    print("Starting navigation...")
                    text_to_speech(engine, "Starting navigation.")
                    threading.Thread(target=open_file, args=("navigation.txt",)).start()  # Start file opening in a separate thread
                    navigation_started = True
                    text_to_speech(engine, "Navigation started.")
                elif "what" in result.lower() and "day" in result.lower():
                    current_day = datetime.datetime.now().strftime("%A")
                    current_month = datetime.datetime.now().strftime("%B")
                    current_year = datetime.datetime.now().strftime("%Y")
                    print("Today is:", current_day, current_month, current_year)
                    text_to_speech(engine, "Today is " + current_day + " " + current_month + " " + current_year)
                elif result.lower() == "goodbye sensation":
                    print("Exiting...")
                    break
                elif "hi" in result.lower() or "hello" in result.lower():
                    text_to_speech(engine, "Hello Apurwa")
                else:
                    text_to_speech(engine, result)  # Call text_to_speech() with the recognized result
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Error: {0}".format(e))

    engine.stop()  # Stop the pyttsx3 engine after exiting the loop

def text_to_speech(engine, text):
    engine.say(text)
    engine.runAndWait()

def open_file(filename):
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found. Creating the file...")
        try:
            with open(filename, "w") as file:
                # Optionally, you can write initial content to the file here
                pass
        except OSError as e:
            print(f"Error creating file: {str(e)}")
        else:
            print(f"File '{filename}' created successfully.")

    try:
        with open(filename, "r") as file:
            # Perform navigation logic here
            pass
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Call the listen_and_recognize() function
listen_and_recognize()
