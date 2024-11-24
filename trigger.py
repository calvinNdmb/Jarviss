#working on it ^^' feel free to fork
import speech_recognition as sr
import subprocess
import sys
recognizer = sr.Recognizer()
trigger_phrase = "jarvis"

def launch_program():
    print("Lancement du programme...")
    #subprocess.run([sys.executable, "main2.py"])

def recognize_speech():
    with sr.Microphone() as source:
        print("Dis quelque chose...")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"Tu as dit : {text}")

            if trigger_phrase in text.lower():
                launch_program()
            if "emergency stop" in text.lower()or "stop jarvis" in text.lower():
                sys.exit()
            else:
                print("Phrase d'activation non détectée.")
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que tu as dit.")
        except sr.RequestError as e:
            print(f"Erreur de reconnaissance vocale : {e}")

