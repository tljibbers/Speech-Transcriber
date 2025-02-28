import tkinter as tk
import speech_recognition as sr
import pyaudio as pa

def workAudio(event):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        label1 = tk.Label(root, text="Talk into your microphone")
        label1.pack()
        audio_text = r.listen(source)
        label2 = tk.Label(root, text="It's over")
        label2.pack()

        try:
            label3 = tk.Label(root, text=r.recognize_google(audio_text))
            label3.pack()
        except:
            label4 = tk.Label(root, text="couldn't understand that")
            label4.pack()

root = tk.Tk('Test', 'TestAgain', 'TestWindow');
labeltest = tk.Label(root, text='Press f to record your audio')
labeltest.pack()
root.bind("<KeyPress>", workAudio)
root.mainloop();


    
