import tkinter as tk
from tkinter import filedialog
from tkinter import Button
import speech_recognition as sr
import pyaudio

switcher = False
def workAudio(event):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        label1 = tk.Label(root, text="Talk into your microphone")
        label1.pack()
        r.adjust_for_ambient_noise(source, 0.2)
        audio_text = r.listen(source, 0, 10)
        label2 = tk.Label(root, text="It's over")
        label2.pack()

        try:
            label3 = tk.Label(root, text=r.recognize_google(audio_text))
            label3.pack()
        except:
            label4 = tk.Label(root, text="couldn't understand that")
            label4.pack()

def audioFileInput():
    file_path = filedialog.askopenfilename()
    if(file_path and checkIfAudioFile(file_path)):
        r = sr.Recognizer()

        with sr.AudioFile(file_path) as source:
            audio = r.record(source, 90)

        text = r.recognize_google(audio)
        print(text)

def checkIfAudioFile(file):
    if(file.lower().endswith('.wav')):
        return True
    if(file.lower().endswith('.mp3')):
        return True



root = tk.Tk('Test', 'TestAgain', 'TestWindow');
root.geometry('300x300')
labeltest = tk.Label(root, text='Press f to record your audio')
labeltest.pack()
button = Button(root, text='Add Audio File (Wav, Mp3)', command=lambda: audioFileInput())
button.pack()
root.bind("<KeyPress>", workAudio)
root.mainloop();


    
