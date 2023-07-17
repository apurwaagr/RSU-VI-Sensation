import os
import handleStop
from handlePrintandSpeak import print_and_speak

def shutdown(self):
    handleStop.stop_sensation(self)
    print_and_speak("Shutting down Sensation...")
    # Additional cleanup or shutdown operations can be added here.
    os._exit(0)