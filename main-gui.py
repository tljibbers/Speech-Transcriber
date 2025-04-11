import tkinter as tk
from tkinter import filedialog
from tkinter import Button
from tkinter.ttk import Progressbar
import pyaudio
import whisper
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

firstTime = False

def audioFileInput(containerFrame):
    for widget in containerFrame.winfo_children():
        widget.destroy()

    #File Explorer gets opened, waiting for an input
    file_path = filedialog.askopenfilename()
    #checks to see if the file path actually exists and to see if its an mp3 or wav file
    if(file_path and checkIfAudioFile(file_path)):
        #Loads in the whisper model
        model = whisper.load_model("large")
        #transcribes the files audio
        result = model.transcribe(file_path)
        print(result['text'])
        #stores the text
        firstAudio = result['text']
        #removes punctuation and lowercases the words
        firstAudioNoPunctuation = firstAudio.lower().replace(',', "").replace('.', "").replace('!', "").replace('?', "")
        #displays text
        label1 = tk.Label(containerFrame, text="Is this what you said: " + firstAudioNoPunctuation, bg="#121313", fg="white", anchor="e", wraplength=480)
        label1.pack(anchor=tk.W)
        #resends the audio to compare whether or not they are the same after a second pass.
        resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription=file_path, containerFrame=containerFrame)
      

def checkIfAudioFile(file):
    #Takes in a string with the file name and checks to see if it ends with .wav or .mp3
    if(file.lower().endswith('.wav')):
        return True
    if(file.lower().endswith('.mp3')):
        return True


def workAudio2(event, containerFrame):
    for widget in containerFrame.winfo_children():
        widget.destroy()
    #Opens up the stream to start recording.
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("begin recording...")

    frames = []
    seconds = 5
    #Records for 5 seconds
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("recording stopped")
    #Closes the stream and ends recording
    stream.stop_stream()
    stream.close()
    #p.terminate()

    #Creates a wav file with the audio
    wf = wave.open("current_voice.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #Loads in the model
    model = whisper.load_model('large')
    #transcribes the files audio
    result = model.transcribe("current_voice.wav")
    print(result['text'])
    #Stores the transcribed text
    firstAudio = result['text']
    #Removes punctuation and lowercases the words
    firstAudioNoPunctuation = firstAudio.lower().replace(',', "").replace('.', "").replace('!', "").replace('?', "")
    #Displays text
    label3 = tk.Label(containerFrame, text="Is this what you said: " + firstAudioNoPunctuation,anchor="e", bg="#121313", fg="white", wraplength=480)
    label3.pack(anchor=tk.W)
    #resends the audio to compare whether or not they are the same after a second pass.
    resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription="current_voice.wav",containerFrame=containerFrame)

def resendAndCompare(firstAudio, transcription, containerFrame):
    label4 = tk.Label(containerFrame, text="Sending the text to the model again to see if it's accurate",anchor='sw', bg="#121313", fg="white", wraplength=480)
    label4.pack(anchor=tk.W)
    #Loads in the model
    model = whisper.load_model('large')
    #Transcribes the Audio
    result = model.transcribe(transcription)
    #Stores the audio text in a variable
    secondAudio = result['text']
    #Removes punctuation and lowercases the words
    secondAudioNoPunctuation = secondAudio.lower().replace(',', "").replace('.', "").replace('!', "").replace('?', "")
    #Displays Text
    label5 = tk.Label(containerFrame, text="On a second go: " + secondAudioNoPunctuation, bg="#121313", fg="white", wraplength=480)
    label5.pack(anchor=tk.W)
    #Compares the audios to each other and checks to see if they are the same or not
    if(firstAudio == secondAudioNoPunctuation):
        label5 = tk.Label(containerFrame, text="They are the same!",justify="left", bg="#121313", fg="white", wraplength=480)
        label5.pack(anchor=tk.W)
        print("they are the same!")
    else:
        print("they aren't the same!")

def createFileInputTkinter():
    global firstTime
    print(firstTime)
    buttonLookForFiles = Button(root, text="Input Files (.mp3, .wav)", command=lambda: audioFileInput(containerFrame))
    containerFrame = tk.LabelFrame(master=root, width=500, height=220, background="#121313")
    if firstTime == False:
        buttonLookForFiles.pack(pady=10)
        containerFrame.pack()
        containerFrame.pack_propagate(False)
        firstTime = True
        


def createAudioInputTkinter():
    containerFrame = tk.LabelFrame(master=root, width=500, height=220, background="#121313")
    labeltest = tk.Label(root, text='Press F To Record Audio', font=("Roboto", 9), bg="#202124", fg="white")
    labeltest.pack(pady=10)
    containerFrame.pack()
    containerFrame.pack_propagate(False)
    root.bind("<f>", lambda event: workAudio2(event, containerFrame))



def clear(containerFrame, buttonLookForFiles):
    containerFrame.destroy()
    buttonLookForFiles.destroy()


root = tk.Tk('SpeechTranscriber', 'SpeechT', ' Speech-Transcriber-v1');
root.geometry('800x300')
root.configure(bg= "#202124")
root.resizable(False, False)
selectorLabel = tk.LabelFrame(master=root, width=200, height=300, background="#121313")
selectorLabel.pack(side='left', fill="both")
mainLogo = tk.Label(selectorLabel, text='SpeechTranscriber', font=("Rubik 15 bold"), bg="#121313", fg="white")
mainLogo.pack()
buttonAudioInput = Button(selectorLabel, text='Record Audio', relief=tk.FLAT, cursor="hand2", bg="#121313", fg="White", command=lambda: createAudioInputTkinter())
buttonAudioInput.pack()
buttonFileInput = Button(selectorLabel, text='Input Files', relief=tk.FLAT, cursor="hand2", bg="#121313", fg="White", command=lambda: createFileInputTkinter())
buttonFileInput.pack()


root.mainloop();




    
