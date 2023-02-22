import speech_recognition as sr 
import json
import random
from gtts import gTTS
from playsound import playsound
from tkinter import *
import tkinter.font as font

root = Tk()			
root.title("FAQ Universitas Brawijaya")
root.geometry('400x100')
myFont = font.Font(size=20)


r = sr.Recognizer()       
#speech = sr.Microphone(device_index=2)  #mic index untuk Raspberry Pi
speech = sr.Microphone()  

def mic_text_doc():     
    recog=None                 
    with speech as source:
        print("Silahkan bicara . . .")
        r.adjust_for_ambient_noise(source)  
        audio = r.listen(source) 

        try:
            recog = r.recognize_google(audio, language = 'ID') 
        except sr.UnknownValueError:               
            print("Maaf, saya belum bisa menangkap itu")
            return

        except sr.RequestError as e:
            print("Service error; {0}".format(e))
            return
    
    print("Anda berbicara : " + recog)   
    
    #recog=input("type your input: ")

    response_founded=False
    count=-1

    if(recog!=None):
        recog=recog.lower()

        for i in range(len(data)):
            if (str(data[i]["tag"]).lower() in recog) or (recog in str(data[i]["tag"]).lower()): 
                count=i
                response_founded=True
                break

            for j in range(len(data[i]["patterns"])): 
                if (str(data[i]["patterns"][j]).lower() in recog) or (recog in str(data[i]["patterns"]).lower()):   
                    count=i
                    response_founded=True
                    break
        
        if response_founded:
            response_gtts=data[count]["response"]
            
            if(len(response_gtts)!=1): 
                random_response=random.randint(1,len(response_gtts))
                response_gtts=response_gtts[random_response-1]

            print("Response:" +str(response_gtts))
            tts=gTTS(str(response_gtts),lang="id") 
            tts.save("response.mp3")
            playsound("response.mp3")

    else:
        return


btn = Button(root, text = 'Tekan untuk mulai bertanya!', bd = '3',command = mic_text_doc,width=40,height=5,bg="blue",fg="yellow")
btn.pack(side = 'top')
btn['font'] = myFont

f = open('faq.json', 'r', encoding="utf8")

data=json.load(f)
data=data["faqs"]
    
while True: 
    root.mainloop()

    



            