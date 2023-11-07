import pyttsx3                           #pip install pyttsx3
import speech_recognition as sr          #pip install SpeechRecognition
import os
import cv2                                #pip install opencv-python
import random
from requests import get                #pip install requests
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes
import requests
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from datetime import datetime,timedelta

user='aadit' # Write your local username 

from fastapi.middleware.cors import CORSMiddleware
import pdb
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query_data(BaseModel):
    query:str

class Ws_message:
    message = None
    client = None
    said_wss = False
    def set_message(message):
        Ws_message.message = message
    
    def set_client(client):
        Ws_message.client = client

    def get_message():
        return Ws_message.message

    def get_client():
        return Ws_message.client
    
class Songs:
    said_wss = False

phone_dict = {
    "vishal":"+9111111111111",
    # Add your contact like this
}

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[2].id)
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    # engine.stop()

#for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=b0b5bb2f6f6c407a9cdd374e1390b0ba'
    article_list = []
    main_page = requests.get(main_url).json()
    print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")
        article_list.append(f"{i+1}. today's {day[i]} news is: {head[i]}\n")
    return article_list

def get_current_time():
    now = datetime.now()
    now = now + timedelta(minutes=1)
    now = now.replace(microsecond=0)
    time = now.time() 
    return time.hour,time.minute

@app.post('/speech_to_text')
def get_query(data:Query_data):
    data = data.dict()
    query = data["query"].lower()
    # works
    if "news" in query:
        speak("please wait sir, feteching the latest news")
        article_list = news()
        return {"message":article_list}

    # works
    elif "open notepad" in query:
        npath = "C:\\Windows\\system32\\notepad.exe"
        os.startfile(npath)
        return {"message":"Opened Notepad!"}
    
    # works
    elif "open command prompt" in query:
        os.system("start cmd")  
        return {"message":"Opened CMD!"}

    # not closing
    elif "open camera" in query:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            k = cv2.waitKey(50)
            print(k)
            if k==5:
                break
        cap.release()
        cv2.destroyAllWindows()
        return {"message":"Camera Opened!"}

    # works
    # Say play songs,then the song name or any random song.
    # Download and setup your songs in .mp3 format in the address given below
    elif  (Songs.said_wss == True) or (("music" in query or "song" in query or "songs" in query or "play" in query)  and ("youtube" not in query)):
        music_dir = f"C:\\Users\{user}\Music"
        songs = [i for i in os.listdir(music_dir) if ".mp3" in i]
        print(songs)
        if Songs.said_wss == False:
            speak("Your songs choices are as follow, you can also play a random song!")
            Songs.said_wss = True
            return {"message":f"Your song choices are {songs}\n or you can play a random song!"}
        if "random" in query:
            song = random.choice(songs)
            print(song)
        else:
            for i in songs:
                if i.split('.')[0] in query:
                    song = i
                    print(song)
                    break
        os.startfile(os.path.join(music_dir, song))
        Songs.said_wss = False
        return {"message":f"Playing Music {song}"}


    elif "ip address" in query:
        ip = get('https://api.ipify.org').text
        speak(f"your IP address is {ip}")
        return {"message":f"your IP address is {ip}"}

        # needs work
    # works
    elif "wikipedia" in query:
        speak("searching wikipedia....")
        query = query.replace("wikipedia","")
        print(query)
        results = wikipedia.summary(query, sentences=2)
        print(results)
        # speak()
        speak(f"according to wikipedia {results}")
        return {"message":results}
        # print(results)
        # needs work   
    
    elif "open youtube" in query:
        webbrowser.open("www.youtube.com")

    # works   
    elif "open facebook" in query:
        webbrowser.open("www.facebook.com")

    # works   
    elif "open stackoverflow" in query:
        query = query.replace("open stackoverflow","")
        search_terms = query.split(' ')

        # ... construct your list of search terms ...
        str = ""
        for term in search_terms:
            str+=f"q={term}&"
        str = str[:-1]
        url = "https://www.stackoverflow.com/search?{}".format(str)
        webbrowser.open_new_tab(url)

    # works
    elif "open google" in query:
        # speak("sir, what should i search on google")
        # cm = takecommand().lower()
        query = query.replace("open google","")
        search_terms = query.split(' ')

        # ... construct your list of search terms ...
        str = ""
        for term in search_terms:
            str+=f"q={term}&"
        str = str[:-1]
        url = "https://www.google.com.tr/search?{}".format(str)
        webbrowser.open_new_tab(url)

    # works
    elif "song on youtube" in query:
        kit.playonyt("closer")
        return {"message":"Task Completed"}
    
    elif "joke" in query:
        speak("Okay! let me think about it")
        joke = pyjokes.get_joke()
        speak(joke)
        return {"message":joke}

# First say whatapp,then tell the client name,then the message
    elif "whatsapp" in query or Ws_message.said_wss:
        if Ws_message.said_wss == False:
            Ws_message.said_wss = True
            return {"message":"Please provide a client name"}
        flag = False
        print('Ws_message.get_client===',Ws_message.get_client())
        if Ws_message.get_client()==None:
            for i in phone_dict.keys():
                print(f"{i}==={query}")
                if i in query:
                    flag = True
                    Ws_message.set_client(i)
            if flag == False:
                return {"message":"Client Name not available; Try another one!"}
            print("flag===",flag)
            return {"message":"Please provide the message to be sent!"}
        if Ws_message.get_message() == None:
            Ws_message.set_message(query)
        if Ws_message.get_client()!=None and Ws_message.get_message()!=None:
            hour,minute = get_current_time()
            client_number = phone_dict[Ws_message.get_client()]
            client_message = Ws_message.get_message().replace("Please provide the message to be sent!","")
            kit.sendwhatmsg(client_number,client_message,hour,minute)
            Ws_message.set_client(None)
            Ws_message.set_message(None)
            Ws_message.said_wss = False
        # speak("Whatsapp messages would take around 120 seconds as per their new policies")
        return {"message":"Whatsapp messages would take around 120 seconds as per their new policies"}

    else:
        return {"message":"Provided query could not be interpreted please provide something else!"}

# if __name__ == '__main__':
#     speak("Hey Morgan here! How Can I assist?")
#     while True:
#     # if 1:
#         query = takecommand().lower()



#         elif "joke" in query:
#             joke = pyjokes.get_joke()
#             speak(joke)
#             sys.exit()


#         elif "shut down the system" in query:
#             os.system("shutdown /s /t 5")

#         elif "restart the system" in query:
#             os.system("shutdown /r /t 5")

#         elif "sleep the system" in query:
#             os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

#         elif "no thanks" in query:
#             speak("thanks for using me sir, have a good day.")
#             sys.exit()

#         elif "song on youtube" in query:
#             kit.playonyt("closer")
#             sys.exit()
