#Speech translation -Realtime audio + TTT + TTS
#Realtime audio input --> realtime text --> text to text translation --> text to speech output


#import statements:
import wave
import random
from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
from spectralcluster import SpectralClusterer
from resemblyzer.audio import sampling_rate
import matplotlib.pyplot as plt
from math import log 
from pydub import AudioSegment
import io

from topic_modelling import topic
#------------------------------------------------------
#Text-to-text translation
from googletrans import Translator

def translate(text):
    print("*** Text to text translation ***")
    
    translator = Translator()
    result = translator.translate(text, src='en', dest='mr')
    
    print("Before translation, language is: " + result.src)
    print("After translation, language is: " + result.dest)
    print("Translated text is: " + result.text)
    
    #calling TTS function
    TTS(result.text)  
    #topic(result.text)
    
#----------------------------------------------------
#Text-to-speech translation
from gtts import gTTS
import os

def TTS(text):
    tts = gTTS(text = text, lang='mr')
    tts.save(r"D:/text_to_speech.mp3")
    os.system(r"D:/text_to_speech.mp3")
    
    #topic(text)
#----------------------------------------------------
#Realtime audio input

#import magic
#print(magic.from_file(audio_text))

def realtime_audio_input():
    import speech_recognition as sr
    
    # Initialize recognizer class (for recognizing the speech)
    
    r = sr.Recognizer()
    
    print("*** Taking realtime audio input ***")
    
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    
    with sr.Microphone() as source:
        
        print("Please Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")      
                
           
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            
        try:
                    # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Realtime audio text: "+ text)
            topic(text)
        except:
            print("Sorry, I did not get that")
                     
        
        #topic(text)
        translate(text)
    
       #clustering(audio_text)
    
       

#---------------------------------------

#Convert flac to wav:

def flac_to_wav(audio_text):
 
    import os    
    
#-----------------------------------------
#Spectral clustering

def clustering():
        audiofile_preprocessed = preprocess_wav(r"C:\\Users\\stile\\Desktop\\longspeaker.wav")
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

#---------------------------------------
#Calling the parent function
realtime_audio_input()

#clustering()


#flac = AudioSegment.from_file(r"C\\Users\\stile\\Desktop\\audio_text.wav", format='wav')
#stream = io.BytesIO()
#output = flac.export(stream, format='wav')

#flac.export(r"C\\Users\\stile\\Desktop\\output_audio.mp3", format="wav")


#file = open(r"C\\Users\\stile\\Desktop\\audio_text.txt", "w") 
#file.write(audio_text) 
#file.close() 



#some_text = open(os.path.join('C:', os.sep, 'Users', 'stile', 'Desktop', 'audio_text.wav')).read()

    #clustering(output)
    

#with open("text_file.txt") as f:lo
 #  contents = f.read()


#flac_to_wav(audio_text)

#r"C\\Users\\stile\\Desktop\\audio_text.wav"


 #file = open(r"C\\Users\\stile\\Desktop\\sound.raw", "w") 
 #file.write(audio_text) 
 #file.close() 
 
 #stream = io.BytesIO()
 #output = audio_text.export(stream, format="wav")

 #audio_text.save(r"C:\Users\stile\Desktop\hope.mp3")

 # import required modules
 #from os import path
 #from pydub import AudioSegment
   
 # assign files
 #input_file = r"D:\text_to_speech.mp3"
 #output_file = r"D:/output.wav"
   
 # convert mp3 file to wav file
 #sound = AudioSegment.from_mp3(input_file)
 #sound.export(output_file, format="wav")
 
 # import required modules
 #from os import path
 #from pydub import AudioSegment
   
 # assign files
 #input_file = r"D:/text_to_speech.mp3"
 #output_file = r"D:/output.wav"
   
 # convert mp3 file to wav file
 #sound = AudioSegment.from_mp3(input_file)
 #sound.export(output_file, format="wav")
 
   #with sr.AudioFile(r"D:/testing.wav") as source:
    #   print("Please Talk")
     #  audio_text = r.record(source)
      # print("Time over, thanks")
      
      #import time

      #t_end = time.time() + 15 * 1
      #while time.time() < t_end: