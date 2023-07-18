#!/usr/bin/env python3

import os
import speech_recognition as sr
import pyttsx3
import threading
from handle_Print_and_Speak import print_and_speak
import handle_Inactive_Sensation
import handle_input_commands

class Sensation:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.sensation_active = False
        self.take_picture_already_processed = False
        #self.current_position_already_processed = False
        self.navigation_already_processed = False

    # to start asr file but doesnt start sensation
    def start(self):
        print_and_speak("Welcome. Please start sensation to experience it.")

        while True:
            try:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.listen(source, timeout=5)
                    result = self.r.recognize_google(audio)
                    print_and_speak("You said: " + result)

                    if self.sensation_active:
                        handle_input_commands.process_command(self,result)
                    else:
                        handle_Inactive_Sensation.handle_inactive_sensation(self, result)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Error:", e)


    def say_hello(self, name):
        print_and_speak("Hello " + name)

sensation = Sensation()
sensation.start()
