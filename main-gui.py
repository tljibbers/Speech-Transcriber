import tkinter as tk
from tkinter import filedialog
from tkinter import Button
import pyaudio
import whisper
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

def audioFileInput():
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
        label1 = tk.Label(root, text="Is this what you said: " + firstAudioNoPunctuation)
        label1.pack()
        #resends the audio to compare whether or not they are the same after a second pass.
        resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription=file_path)
      

def checkIfAudioFile(file):
    #Takes in a string with the file name and checks to see if it ends with .wav or .mp3
    if(file.lower().endswith('.wav')):
        return True
    if(file.lower().endswith('.mp3')):
        return True


def workAudio2(event):
    #Opens up the stream to start recording.
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("begin recording...")
    label1 = tk.Label(root, text="Talk into your microphone")
    label1.pack()
    frames = []
    seconds = 5
    #Records for 5 seconds
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("recording stopped")
    label2 = tk.Label(root, text="It's over")
    label2.pack()
    #Closes the stream and ends recording
    stream.stop_stream()
    stream.close()
    p.terminate()

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
    label3 = tk.Label(root, text="Is this what you said: " + firstAudioNoPunctuation)
    label3.pack()
    #resends the audio to compare whether or not they are the same after a second pass.
    resendAndCompare(firstAudio=firstAudioNoPunctuation, transcription="current_voice.wav")

def resendAndCompare(firstAudio, transcription):
    label4 = tk.Label(root, text="Sending the text to the model again to see if it's accurate")
    label4.pack()
    #Loads in the model
    model = whisper.load_model('large')
    #Transcribes the Audio
    result = model.transcribe(transcription)
    #Stores the audio text in a variable
    secondAudio = result['text']
    #Removes punctuation and lowercases the words
    secondAudioNoPunctuation = secondAudio.lower().replace(',', "").replace('.', "").replace('!', "").replace('?', "")
    #Displays Text
    label5 = tk.Label(root, text="On a second go: " + secondAudioNoPunctuation)
    label5.pack()
    #Compares the audios to each other and checks to see if they are the same or not
    if(firstAudio == secondAudioNoPunctuation):
        label5 = tk.Label(root, text="They are the same!")
        label5.pack()
        print("they are the same!")
    else:
        print("they aren't the same!")



root = tk.Tk('Test', 'TestAgain', 'Speech Transcriber');
root.geometry('300x300')
labeltest = tk.Label(root, text='Press f to record your audio')
labeltest.pack()
button = Button(root, text='Add Audio File (Wav, Mp3)', command=lambda: audioFileInput())
button.pack()
root.bind("<KeyPress>", workAudio2)
root.mainloop();



    
