import tkinter as tk
from tkinter import filedialog
from tkinter import Button
import speech_recognition as sr
import pyaudio
import whisper
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()


switcher = False

def audioFileInput():
    file_path = filedialog.askopenfilename()
    if(file_path and checkIfAudioFile(file_path)):
        model = whisper.load_model("turbo")
        result = model.transcribe(file_path)
        print(result['text'])
        firstAudio = result['text']
        firstAudioNoPunctuation = firstAudio.lower().replace(',', "").replace('.', "")
        label1 = tk.Label(root, text="Is this what you said: " + firstAudioNoPunctuation)
        label1.pack()
        resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription=file_path)
      

def checkIfAudioFile(file):
    if(file.lower().endswith('.wav')):
        return True
    if(file.lower().endswith('.mp3')):
        return True


def workAudio2(event):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("begin recording...")
    label1 = tk.Label(root, text="Talk into your microphone")
    label1.pack()
    frames = []
    seconds = 5
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("recording stopped")
    label2 = tk.Label(root, text="It's over")
    label2.pack()
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("current_voice.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    model = whisper.load_model('large')
    result = model.transcribe("current_voice.wav")
    print(result['text'])
    firstAudio = result['text']
    firstAudioNoPunctuation = firstAudio.lower().replace(',', "").replace('.', "")
    label3 = tk.Label(root, text="Is this what you said: " + firstAudioNoPunctuation)
    label3.pack()
    resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription="current_voice.wav")

def resendAndCompare(firstAudio, transcription):
    label4 = tk.Label(root, text="Sending the text to the model again to see if it's accurate")
    label4.pack()
    model = whisper.load_model('large')
    result = model.transcribe(transcription)
    secondAudio = result['text']
    secondAudioNoPunctuation = secondAudio.lower().replace(',', "").replace('.', "")
    label5 = tk.Label(root, text="On a second go: " + secondAudioNoPunctuation)
    label5.pack()
    if(firstAudio == secondAudioNoPunctuation):
        label5 = tk.Label(root, text="They are the same!")
        label5.pack()
        print("they are the same!")
    else:
        print("they aren't the same!")



root = tk.Tk('Test', 'TestAgain', 'TestWindow');
root.geometry('300x300')
labeltest = tk.Label(root, text='Press f to record your audio')
labeltest.pack()
button = Button(root, text='Add Audio File (Wav, Mp3)', command=lambda: audioFileInput())
button.pack()
root.bind("<KeyPress>", workAudio2)
root.mainloop();



    
