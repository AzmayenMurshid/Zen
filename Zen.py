import speech_recognition as sr
import pyttsx3 # text to speech
import webbrowser
from datetime import date, timedelta, datetime
import serial  # used to communicate with Arduino board
import pyowm  # used to tell the weather
from Keys import OPENWEATHER  # Keys.py is where I store all my API keys ZEN will use
import operator  # used for math operations
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory
import pyjokes  # used to tell jokes
import threading # used to run threads
import time
import pyautogui # Auto mouse movement
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import random

from volumes import volume_settings


# Speech Recognition Constants
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Python Text-to-Speech (pyttsx3) Constants
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)

# Wake word in Listen Function
WAKE = "Zen"
autopilot = False

# Used to store user commands for analysis
CONVERSATION_LOG = "Conversation Log.txt"

# Initial analysis of words that would typically require a Google search
SEARCH_WORDS = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}

# Establish serial connection for arduino board
try:
    ser = serial.Serial('com3', 9600)
    LED = True
except Exception as e:
    print("LEDs are not connected. There will be no lighting support.")
    # If the LEDs aren't connected this will allow the program to skip the LED commands.
    LED = False
    pass

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

class Zen:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    # Used to hear the commands after the wake word has been said
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # May reduce the time out in the future
                audio = recognizer.listen(source, timeout=2.0)
                command = recognizer.recognize_google(audio)
                s.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to speak to the user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Used to open the browser or specific folders
    def open_things(self, command):
        # Will need to expand on "open" commands
        if command == "open youtube":
            s.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")
            pass

        elif command == "open facebook":
            s.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
            pass

        elif command == "open google":
            s.speak("Opening Google.")
            webbrowser.open("https://www.google.com")
            pass
        
        elif command == "open instagram":
            s.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com")
            pass

        elif command == "open twitter":
            s.speak("Opening Twitter.")
            webbrowser.open("https://www.twitter.com")
            pass
        
        elif command == "open github":
            s.speak("Opening GitHub.")
            webbrowser.open("https://www.github.com/AzmayenMurshid")
            pass

        elif command == "open google drive":
            s.speak("Opening Google Drive.")
            webbrowser.open("https://drive.google.com")
            pass
        
        elif command == "open google maps":
            s.speak("Opening Google Maps.")
            webbrowser.open("https://www.google.com/maps")
            pass

        elif command == "open google classroom":
            s.speak("Opening Google Classroom.")
            webbrowser.open("https://classroom.google.com")
            pass
        
        elif command == "open spotify":
            s.speak("Opening Spotify.")
            webbrowser.open("https://www.spotify.com")
            pass

        elif command == "open amazon":
            s.speak("Opening Amazon.")
            webbrowser.open("https://www.amazon.com")
            pass
        
        elif command == "open ebay":
            s.speak("Opening Ebay.")
            webbrowser.open("https://www.ebay.com")
            pass

        elif command == "open my documents":
            s.speak("Opening My Documents.")
            os.startfile("D:/")
            pass

        elif command == "open my downloads folder":
            s.speak("Opening your downloads folder.")
            os.startfile("D:\Downloads folder")
            pass
        
        elif command == "open google slides":
            s.speak("Opening Google Slides.")
            webbrowser.open("https://docs.google.com/presentation/")
            pass

        elif command == "open google docs":
            s.speak("Opening Google Docs.")
            webbrowser.open("https://docs.google.com/document/")
            pass

        else:
            s.speak("I don't know how to open that yet.")
            pass

    # Used to track the date of the conversation, may need to add the time in the future
    def start_conversation_log(self):
        today = str(date.today())
        today = today
        with open(CONVERSATION_LOG, "a") as f:
            f.write("Conversation started on: " + today + "\n")

    # Writes each command from the user to the conversation log
    def remember(self, command):
        with open(CONVERSATION_LOG, "a") as f:
            f.write("User: " + command + "\n")

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        if "today" in command:
            s.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif command == "what time is it":
            s.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

        elif "yesterday" in command:
            date_intent = today - timedelta(days=1)
            return date_intent

        elif "this time last year" in command:
            current_year = today.year

            if current_year % 4 == 0:
                days_in_current_year = 366

            else:
                days_in_current_year = 365
            date_intent = today - timedelta(days=days_in_current_year)
            return date_intent

        elif "last week" in command:
            date_intent = today - timedelta(days=7)
            return date_intent
        else:
            pass

    def get_weather(self, command):
        home = 'Bandar Sunway, Malaysia'
        owm = pyowm.OWM(OPENWEATHER)
        mgr = owm.weather_manager()

        if "now" in command:
            observation = mgr.weather_at_place(home)
            w = observation.weather
            temp = w.temperature('fahrenheit')
            status = w.detailed_status
            s.speak("It is currently " + str(int(temp['temp'])) + " degrees and " + status)

        else:
            s.speak("I haven't programmed that yet.")

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            'divided': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
            '^': operator.xor,
        }[op]

    # We'll need a list to perform the math
    def do_math(self, li):
        # passes the second item in our list to get the built-in function operand
        op = self.get_operator(li[1])
        # changes the strings in the list to integers
        int1, int2 = int(li[0]), int(li[2])
        # this uses the operand from the get_operator function against the two intengers
        result = op(int1, int2)
        s.speak(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))

    # Checks "what is" to see if we're doing math
    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        # First, we'll make a list a out of the string
        li = list(command.split(" "))
        # Then we'll delete the "what" and "is" from the list
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "what is the date today" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        s.speak("Here is what I found.")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    def sound_control(self, command):
        global volume
        if command.startswith('set volume to'):
            vol = int(command[13:])
            if vol in volume_settings:
                volume.SetMasterVolumeLevel(vol, None)
            else:
                s.speak("That isn't an option")

    # Analyzes the command
    def analyze(self, command):
        try:

            if command.startswith('open'):
                self.open_things(command)

            elif command == "introduce yourself":
                s.speak("I am {}. I'm an A.I. assistant.".format(WAKE))

            elif command == "shut down" or command == "shut down computer":
                s.speak("Shutting down.")
                os.system("shutdown /s /t 1")
                pass

            elif command == "lock computer" or command == "lock":
                s.speak("Locking computer.")
                os.system("rundll32.exe user32.dll,LockWorkStation")
                pass

            elif command == "unlock computer" or command == "unlock" or command == "look alive":
                s.speak("Unlocking computer.")
                os.system("rundll32.exe user32.dll,UnlockWorkStation")
                pass

            elif command == "restart computer":
                s.speak("Restarting computer.")
                os.system("shutdown /r /t 1")
                pass

            elif command == "sleep":
                s.speak("Sleeping computer.")
                os.system("shutdown /h /t 1")
                pass

            elif command == "clear windows":
                s.speak("Clearing windows.")
                os.system("cls")
                pass
                
            elif command == "minimize windows":
                s.speak("Minimizing windows.")
                os.system("taskkill /f /im explorer.exe")
                pass

            elif command == "what time is it":
                self.understand_time(command)

            elif command == "exit program" or command == "exit" or command == "quit":
                s.speak("Pleasure to help you! Goodbye.")
                exit()
            
            elif command == "auto-pilot" or command == "take over":
                s.speak("Autopilot activated")
                global autopilot
                autopilot = True

                while autopilot:
                    x = random.randint(0, 1000)
                    y = random.randint(0, 1000)
                    pyautogui.moveTo(x, y)

                    #localtime = time.localtime()
                    #result = time.strftime("%H:%M:%S %p", localtime)
        
                return autopilot

            elif command == "deactivate autopilot" or command == "stop autopilot":
                s.speak("Autopilot deactivated")
                autopilot = False
                return autopilot

            elif command == "how are you":
                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]
                # selects a random choice of greetings
                greeting = random.choice(current_feelings)
                s.speak(greeting)

            elif "weather" in command:
                self.get_weather(command)

            elif "what is" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            else:
                s.speak("I don't know how to do that yet.")

                if LED:
                    listening_byte = "H"  # H matches the Arduino sketch code for the green color
                    ser.write(listening_byte.encode("ascii"))  # encodes and sends the serial byte
        except TypeError:
            print("Warning: You're getting a TypeError somewhere.")
            pass
        except AttributeError:
            print("Warning: You're getting an Attribute Error somewhere.")
            pass

    # Used to listen for the wake word
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening.")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=2.0)
                    response = recognizer.recognize_google(audio)

                    if response == WAKE:
                        responses = ["Yes?", "What can I help you with?"]
                        s.speak(random.choice(responses))
                        if LED:
                            listening_byte = "L"  # L matches the Arduino sketch code for the blue color
                            ser.write(listening_byte.encode("ascii"))  # encodes and sends the serial byte
                        s.speak("How can I help you?")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")


s = Zen()
s.start_conversation_log()
# Used to prevent people from asking the same thing over and over
previous_response = ""
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)

    if command == previous_response:
        s.speak("You already asked that. Ask again if you want to do that again.")
        previous_command = ""
        response = s.listen(recognizer, microphone)
        command = s.hear(recognizer, microphone, response)
    s.analyze(command)
    previous_response = command
