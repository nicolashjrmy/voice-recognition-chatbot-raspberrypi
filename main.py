import json
import random
import io
import torch
import pygame
from gtts import gTTS
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import speech_recognition as sr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from tkinter import *
import tkinter.font as font
from pydub import AudioSegment

root = Tk()
root.title("FAQ Universitas Brawijaya")
root.geometry('400x100')
myFont = font.Font(size=20)

r = sr.Recognizer()
#speech = sr.Microphone(device_index=2) #mic index untuk raspberry
speech = sr.Microphone(sample_rate=16000)
pygame.mixer.init()

tokenizer = Wav2Vec2Processor.from_pretrained('indonesian-nlp/wav2vec2-large-xlsr-indonesian')
model = Wav2Vec2ForCTC.from_pretrained('indonesian-nlp/wav2vec2-large-xlsr-indonesian')

with open('faq.json', 'r', encoding="utf8") as f:
    faqs = json.load(f)['faqs']

def preprocess(text):
    text = ' '.join(text)  # Join list of strings into a single string
    text = text.lower()
    return text

X = [preprocess(faq['patterns']) for faq in faqs]
y = [faq['tag'] for faq in faqs]

# train model
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X)
clf = MultinomialNB()
clf.fit(X_train_vec, y)

def mic_text_doc():
    with speech as source:
        print("Silahkan bicara . . .")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            data = io.BytesIO(audio.get_wav_data())
            clip = AudioSegment.from_wav(data)
            x = torch.FloatTensor(clip.get_array_of_samples())

            inputs = tokenizer(x, sampling_rate=16000, return_tensors='pt', padding='longest').input_values
            logits = model(inputs).logits
            tokens = torch.argmax(logits, axis=-1)
            recog = tokenizer.batch_decode(tokens)[0]

        except sr.UnknownValueError:
            print("Maaf, saya belum bisa menangkap itu")
            return

        except sr.RequestError as e:
            print("Service error; {0}".format(e))
            return

    print("Anda berbicara: " + recog)

    response_founded=False

    if(recog!=None):
        recog=recog.lower()
        recog_vec = vectorizer.transform([recog])
        tag = clf.predict(recog_vec)[0]

        for faq in faqs:
            if faq['tag'] == tag:
                response_founded = True
                responses = faq['response']
                response = random.choice(responses)
                print("Response: " + response)
                tts = gTTS(response, lang="id")
                tts.save("response.mp3")
                pygame.mixer.music.load("response.mp3")
                pygame.mixer.music.play()
                break

    if not response_founded:
        print("Maaf, pertanyaan tidak ditemukan")

btn = Button(root, text='Tekan untuk mulai bertanya!', bd='3', command=mic_text_doc, width=40, height=5, bg="blue", fg="yellow")
btn.pack(side='top')
btn['font'] = myFont

root.mainloop()
