import os
import speech_recognition as sr
import pyttsx3
import datetime
import threading
import geocoder

class Sensation:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.sensation_active = False

    def start(self):
        self.print_and_speak("Welcome to Sensation. You can start speaking now.")

        while True:
            try:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.listen(source, timeout=5)
                    result = self.r.recognize_google(audio)
                    #print("You spoke:", result)
                    self.print_and_speak("You said: " + result)

                    if self.sensation_active:
                        self.process_command(result)
                    else:
                        self.handle_inactive_sensation(result)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Error:", e)

    def process_command(self, command):
        if "what" in command.lower() and "time" in command.lower():
            self.get_current_time()
        elif "position" in command.lower() or "location" in command.lower():
            self.get_current_position()
        elif "picture" in command.lower() or "photo" in command.lower():
            self.take_picture()
        elif "say hi to" in command.lower():
            name = command.lower().split("say hi to")[1].strip()
            self.say_hello(name)
        elif command.lower() == "stop sensation":
            self.stop_sensation()
        elif command.lower() == "shut down sensation":
            self.shutdown()
        else:
            self.print_and_speak("Invalid command.")

    def handle_inactive_sensation(self, command):
        if command.lower() == "start sensation":
            if not self.sensation_active:
                self.start_sensation()
            else:
                self.print_and_speak("Sensation is already active.")
        elif command.lower() == "shut down sensation":
            self.shutdown()
        else:
            self.print_and_speak("Sensation is not active. Start Sensation to proceed.")

    def start_sensation(self):
        self.sensation_active = True
        self.print_and_speak("Sensation started.")

    def stop_sensation(self):
        if self.sensation_active:
            self.sensation_active = False
            self.print_and_speak("Sensation stopped.")
        else:
            self.print_and_speak("Sensation is not active.")

    def shutdown(self):
        self.stop_sensation()
        self.print_and_speak("Shutting down Sensation...")
        # Additional cleanup or shutdown operations can be added here.
        os._exit(0)

    def print_and_speak(self, message):
        print(message)
        self.engine.say(message)
        self.engine.runAndWait()

    def get_current_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.print_and_speak("The current time is " + current_time)

    def get_current_position(self):
        g = geocoder.ip('me')
        if g.ok:
            city = g.city if g.city else ""
            state = g.state if g.state else ""
            country = g.country if g.country else ""
            street = g.street if g.street else ""
            position = f"{street}, {city}, {state}"
        else:
            position = "Unable to retrieve current position"
        self.print_and_speak("Your current position is " + position)

    def take_picture(self):
        # Implementation for taking a picture can be added here
        self.print_and_speak("Picture was successfully stored.")

    def say_hello(self, name):
        self.print_and_speak("Hello " + name)

sensation = Sensation()
sensation.start()
