# importing the required libraries and packages

import wave
import random
from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
from spectralcluster import SpectralClusterer
from resemblyzer.audio import sampling_rate
import matplotlib.pyplot as plt
from math import log 
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os
#-------------------------thr-----------------PART 1-----------------------------------------------

# accessing the location of audio file to be processed
#os.system(r'start C:\Users\stile\Desktop')
filename = input("Please enter the name of your file -")
audiofile_raw = Path(r"C:\\Users\\stile\\Desktop\\" + filename + '.wav')

audiofile_preprocessed = preprocess_wav(audiofile_raw)
encoder = VoiceEncoder("cpu")
_, cont_embeds, wav_splits = encoder.embed_utterance(audiofile_preprocessed, return_partials = True, rate = 16)
print(cont_embeds.shape)

# accepting number of speakers from user
no_of_speakers = int(input("Please enter total number of speakers -"))

# clustering the embedded segments using spectral clustering 
clusterer = SpectralClusterer(min_clusters=no_of_speakers, max_clusters=5)
labels = clusterer.predict(cont_embeds)

# creating a tuple list called labelling;
# each tuple will consist - Speaker, start tme, end time
def create_labelling(labels,wav_splits):
    times = [((speaker.start + speaker.stop) / 2) / sampling_rate for speaker in wav_splits]
    labelling = []
    start_time = 0

    for i,time in enumerate(times):
        if i>0 and labels[i]!=labels[i-1]:
            temp = [str(labels[i-1]),start_time,time]
            labelling.append(tuple(temp))
            start_time = time
        if i==len(times)-1:
            temp = [str(labels[i]),start_time,time]
            labelling.append(tuple(temp))

    return labelling
 
# printing the tuple list (helps to identify distint speakers)
labelling = create_labelling(labels,wav_splits)
print('Speaker ID, start-time, end-time')
print(labelling)

# to generate a 2-axis graph, combining start-time and end-time as Timeline to be plotted against Speaker ID 
element_list = [(elem1, elem2, log(elem3)) for elem1, elem2, elem3 in labelling]

# visualising the clusters in the form of a scatter plot (time vs speakers) 
plt.scatter(*zip(*element_list), color = 'red')
plt.xlabel('Speaker ID')
plt.ylabel('Timeline (in seconds)')
plt.show

#------------------------------------------PART 2-----------------------------------------------

#Text-to-text translation
def TTT(text):
    #with open("text_file.txt") as f:lo
     #  contents = f.read()

    translator = Translator(to_lang="Hindi")
    translation = translator.translate(text)
    print(translation)
    
from googletrans import Translator

def translate(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='hi')
    
    print(result.src)
    print(result.dest)
    print(result.text)
    
    TTS(result.text)
   
#Text-to-speech translation
def TTS(text):
    tts = gTTS(text = text, lang='hi')
    tts.save(r"C:\Users\stile\Desktop\text_to_speech.mp3")
    os.system(r"C:\Users\stile\Desktop\text_to_speech.mp3")

# Initialize recognizer class (for recognizing the speech)
#speech to text using pre-recorded audio files
def speech_to_text(random_number, speaker_id):
    with sr.AudioFile(r'C:\Users\stile\Desktop\audiofile_slice' + random_number + '.wav') as source:
    
        audio_text = sr.Recognizer().record(source)
    
        # recoginize() method will throw a request error if the API is unreachable, hence using exception handling
        try:
        
                # using google speech recognition API + python speech recognition library
                text = sr.Recognizer().recognize_google(audio_text)
                print('Speaker: ' + speaker_id)
                print(text)
                
                #file = open("text_file.txt", "w") srish
                #file.write(text) 
                #file.close() 
                
        except:
                print('Transcription failure, try again :/')
                
                

        #translate(text)
        #TTS(text)
        
#speech to text for realtime audio files
def realtime_audio():
    r = sr.Recognizer()
    
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        
        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Text: "+ text)
        except:
             print("Sorry, I did not get that")
             
        translate(text)
        TTS(text)

# splitting given wave file into multiple files for each speaker 
def wavesplitter(start, end, speaker_id):
    # file to extract the snippet from
    with wave.open(r"C:\\Users\\stile\\Desktop\\" + filename + '.wav', "rb") as infile:
        
        # get file data
        nchannels = infile.getnchannels()
        sampwidth = infile.getsampwidth()
        framerate = infile.getframerate()
        
        # set position in wave to start of segment
        infile.setpos(int(start * framerate))
        
        # extract data
        data = infile.readframes(int((end - start) * framerate))

        # write the extracted data to a new file
        random_number = str(random.randint(1,1000))
        
        with wave.open(r'C:\Users\stile\Desktop\audiofile_slice' + random_number + '.wav', 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)
            
        # calling speech-to-text method within the wave splitter function
        speech_to_text(random_number, speaker_id)
        #realtime_audio()
        
for x in labelling:
  # iterate in each tuple element
  start = x[1]
  end = x[2]
  speaker_id = x[0]
  wavesplitter(start, end, speaker_id)
   
  
#------------------------------------------------ end of program ----------------------------------
#Text to text module (works for hindi, marathi, english)
