#!/usr/bin/env python3

import os
import speech_recognition as sr
import pyttsx3
#import datetime
import threading
#import geocoder
import handleLocation
import handlePicture
import handleTime
import handleShutdown
import handleStop
import handleStart
from handlePrintandSpeak import print_and_speak

class Sensation:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.sensation_active = False
        self.take_picture_already_processed = False
        self.current_position_already_processed = False

    def start(self):
        print_and_speak("Welcome to Sensation. Please start sensation.")

        while True:
            try:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.listen(source, timeout=5)
                    result = self.r.recognize_google(audio)
                    #print("You spoke:", result)
                    print_and_speak("You said: " + result)

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
            handleTime.get_current_time(self)
        elif "position" in command.lower() or "location" in command.lower():
            if self.current_position_already_processed is False:
                self.current_position_already_processed = True
                handleLocation.get_current_position(self)
            else:
                print_and_speak("Current Position command is already processed. Skipping this command")
        elif "picture" in command.lower() or "photo" in command.lower():
            if self.take_picture_already_processed is False:
                self.take_picture_already_processed = True
                handlePicture.take_picture(self)
            else:
                print_and_speak("Take picture command is already processed. Skipping this command")
        elif "say hi to" in command.lower():
            name = command.lower().split("say hi to")[1].strip()
            self.say_hello(name)
        elif command.lower() == "stop sensation" or command.lower() == "close sensation":
            handleStop.stop_sensation(self)
        elif command.lower() == "shut down sensation":
            handleShutdown.shutdown(self)
        else:
            print_and_speak("Invalid command.")

    def handle_inactive_sensation(self, command):
        if "start" in command.lower() or "hello" in command.lower() or ("sensation" in command.lower() and command.lower() != "shut down sensation" and command.lower()!= "stop sensation"):
            if not self.sensation_active:
                handleStart.start_sensation(self)
                self.take_picture_already_processed = False
                self.current_position_already_processed = False
            else:
                print_and_speak("Sensation is already active.")
        elif command.lower() == "shut down sensation":
            handleShutdown.shutdown(self)
        else:
            print_and_speak("Sensation is not active. Start Sensation to proceed.")



    def say_hello(self, name):
        print_and_speak("Hello " + name)

sensation = Sensation()
sensation.start()
