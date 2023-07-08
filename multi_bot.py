import datetime
import requests
import os
import telebot
import random
import imaplib
import email
from PIL import Image
from PyPDF2 import PdfFileMerger
import re
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from dotenv import load_dotenv
#
#
# INITIALIZE ALL REQUIRED KEYS AND CREDENTIALS BELOW FOR PROPER WORKING OF BOT
#
#
from cryptography.fernet import Fernet
#Variable initializing

is_weather="0"
sos_active="0"
reels_active="0"
string=" "
cl = Client()
tempdir=os.getcwd()
Credentials={}


#Code for handling credential encryption and decryption
a=1
if a==1:
    try:
        with open('crypt.key', 'rb') as filekey:
            key = filekey.read()
        
        fernet = Fernet(key)
        with open('.env', 'rb') as file:
            original = file.read()
        decrypted = fernet.decrypt(original)
        with open('.env', 'wb+') as decrypted_file:
            decrypted_file.write(decrypted)
            dnc=decrypted_file.read()
            print("decrypted")
    except :
        print("Invalid Key or Already decrypted")
    
    #loading credentials and keys from env file
    load_dotenv(tempdir+"\.env")
    username=os.getenv("E-mail_for_checking_email")
    password=os.getenv("Password_for_checking_mail")
    TELE_API_KEY = os.getenv("Telegram_bot_API")
    print(TELE_API_KEY)
    OW_API = os.getenv("Open_Weather_API")
    with open(".env","r") as credentials:
        Credentials=credentials.readlines()
        print(Credentials)
    key = Fernet.generate_key()
    with open('crypt.key', 'wb') as filekey:
        filekey.write(key)
        print("new key gen")
    try:
        with open('crypt.key', 'rb') as filekey:
            key = filekey.read()        
        fernet = Fernet(key)
        with open('.env', 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open('.env', 'wb+') as encrypted_file:
            encrypted_file.write(encrypted)
            enc=encrypted_file.read()
            print("encrypted")
    except:
        print("encrypt failed")    

print(Credentials)

# Directory creation and verification
def init_dirs():
    req_dir=("reels","temppdf","merged","tempimg")
    path=os.getcwd()
    try:
        for i in req_dir:
            os.mkdir(path+"\\"+i)
            print("required dirs created")
    except FileExistsError:
        print("dirs already exists")
init_dirs()
#Bot initialization
bot = telebot.TeleBot(TELE_API_KEY)
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
bot = telebot.TeleBot(TELE_API_KEY)
# Initialize Joke.txt Dataset
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list
#Code for file handling (jpg2pdf) 
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    file_name = 'tempimg/' + file.file_path.split('/')[-1]
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Photo saved!")
    print ("img in temp..")
#Code  for handling /commands
@bot.message_handler(commands=["commands"])
def message(message):
    commands="""/start - greet to check life of the bot
/tell_joke - returns a random joke
/weather - view the weather of the city
/check_email - check email for unread messages
/jpg2pdf - converts images to pdf
/sos - emergency contact number
/commands - return list of commands
"""
    bot.reply_to(message,"Here are the list of commands \n"+commands)
#Code to handle jpg2pdf conversion
@bot.message_handler(commands=["jpg2pdf"])
def convert(message):
    dir=tempdir+"\\tempimg"
    a=os.listdir(dir)
    print(a)
    for i in a:
        dirf=tempdir+"\\tempimg\\"+i
        dirsav=tempdir+"\\temppdf\\"+i+".pdf"
        im=Image.open(dirf)
        imc=im.convert('RGB')
        imc.save(dirsav)
    pdfs_dir =tempdir+"\\temppdf\\"  
    merged_file_name = 'merged\\merged.pdf'
    pdf_merger = PdfFileMerger()
    for filename in os.listdir(pdfs_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdfs_dir, filename)
            with open(file_path, 'rb') as pdf_file:
                pdf_merger.append(pdf_file)
    with open(merged_file_name, 'wb') as merged_file:
        pdf_merger.write(merged_file)
    print('PDFs merged successfully!')
    with open("merged\\merged.pdf", 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file)
        bot.reply_to(message, "PDF file sent")
    def junk_removal():
        os.remove("merged\\merged.pdf")
        print("merged pdf deleted....")
        for i in a:
            os.remove("tempimg\\"+i)
        print("temp img is deleted")
        for i in a:
            os.remove("temppdf\\"+i+".pdf")
        print("temp pdf is deleted..")
    junk_removal()
#Code to handle /check_email command
@bot.message_handler(commands=["check_email"])
def check_email(message):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    result, data = mail.search(None, "UNSEEN")
    unread_count = len(data[0].split())
    bot.reply_to(message, f"You have {unread_count} unread emails.")
    mail.logout()
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit
#Code to handle /tell_joke command
@bot.message_handler(commands=["tell_joke"])
def tell_joke(message):
    i=random.randrange(0,1600)
    joke=open("joke.txt","r")
    data=joke.read().split(",") 
    data=remove(data)
    a=data[i]
    print(a)
    bot.reply_to(message, a)
#Code to handle /start command
@bot.message_handler(commands=["start"])
def greet(message):
    bot.reply_to(message,"Hey! Hows it going?")
#Combined Code to handle weather , sos , reels command
@bot.message_handler(commands=["weather","sos","reels"])
def weather(message):
    status=str(message.text)
    print(status)
    global sos_active
    global is_weather
    global reels_active
    if  status=="/weather":
        is_weather="1"
        bot.reply_to(message, "Set City")
    elif status=="/sos":
        sos_active="1"
        bot.reply_to(message,"Enter Country Name")
    else:
        reels_active="1"
        bot.reply_to(message,"Enter reels link")  
#Code to handle execution of weather , sos, reels  
@bot.message_handler(func=lambda m: True)
def city(message):
    global is_weather
    global sos_active
    global reels_active
    if is_weather == "1":
        global CITY
        CITY = str(message.text)
        print(CITY)
        url = BASE_URL + "appid=" + OW_API + "&q=" + CITY
        print(url)
        response = requests.get(url).json()
        print(response)
        error_responce={"cod":"404","message":"city not found"}
        if response==error_responce:
            print("invalid city")
            bot.reply_to(message, "Enter a valid city name")
        else:
            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = response["main"]['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            wind_speed = response['wind']['speed']
            humidity = response['main']['humidity']
            description = response['weather'][0]['description']
            print(description)
            if (description == 'broken clouds'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'brokenclouds.jpg', 'rb'))
            elif (description == 'few clouds'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'fewclouds.jpg', 'rb'))
            elif (description == 'overcast clouds'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'overcastclouds.jpg', 'rb'))
            elif (description == 'scattered clouds'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'scatteredclouds.jpg', 'rb'))
            elif (description == 'clearsky'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'clearsky.jpg', 'rb'))
            elif (description == 'mist'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'mist.jpg', 'rb'))
            elif (description == 'haze'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'haze.jpg', 'rb'))
            elif (description == 'light rain'):
                bot.send_photo(chat_id=message.chat.id, photo=open(tempdir+"\\img\\"+'light_rain.jpg', 'rb'))
            sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
            t = (f"Temperature in {CITY}: {temp_celsius:.2f}*C or {temp_fahrenheit:.2f}*F")
            flc = (f"Temperature in {CITY}: {feels_like_celsius:.2f}*C or {feels_like_fahrenheit:.2f}*F")
            H = (f"Humidity in {CITY}: {humidity}%")
            h = (f"Wind Speed in {CITY}: {wind_speed} m/s")
            gw = (f"General Weather in {CITY} at {sunrise_time} local time: {description}")
            sr = (f"Sun rises in {CITY} at {sunrise_time} local time.")
            st = (f"Sun sets in {CITY} at {sunset_time} local time.")
            bot.reply_to(message, t)
            bot.send_message(message.chat.id, flc)
            bot.send_message(message.chat.id, H)
            bot.send_message(message.chat.id, h)
            bot.send_message(message.chat.id, gw)
            bot.send_message(message.chat.id, sr)
            bot.send_message(message.chat.id, st)
        is_weather="0"
    elif sos_active=="1":
        f=open("sos_list.txt","r")
        data=f.readlines()
        state=str(message.text)
        state=state.capitalize()
        print(state)
        for i in data:
            tmplist=i.split()
            if state==tmplist[0]:
                tmplist.pop()
                tmplist.pop(0)
                tmplist.pop(0)
                tmplist.pop(0)
                sos="Emergency Numbers For "+state+"\nAmbulance = "+tmplist[0]+"\nFire = "+tmplist[1]+"\nPolice = "+tmplist[2]
                bot.reply_to(message,sos)
        sos_active="0"
    elif reels_active=="1":
        ori_reel=str(message.text)
        reel=ori_reel.split("https://www.instagram.com/reel/")
        base_url="https://www.ddinstagram.com/reel/"
        Reel_to_send=base_url+reel[1]
        Reel_markup="[REEL]("+Reel_to_send+")"
        print(Reel_markup)
        bot.reply_to(message,Reel_markup)
    else:
        status = str(message.text)
        if status.startswith("https://www.instagram.com/reel/"):
            print("reel")
            ori_reel=str(message.text)
            reel=ori_reel.split("https://www.instagram.com/reel/")
            base_url="https://www.ddinstagram.com/reel/"
            Reel_to_send=base_url+reel[1]
            Reel_markup=Reel_to_send
            print(Reel_markup)
            bot.reply_to(message,Reel_markup)
        elif status.startswith("https://www.instagram.com/p/"):
            print("post")
            ori_post=str(message.text)
            reel=ori_post.split("https://www.instagram.com/p/")
            base_url="https://www.ddinstagram.com/p/"
            Post_to_send=base_url+reel[1]
            Post_markup=Post_to_send
            print(Post_markup)
            bot.reply_to(message,Post_markup)
        else:
            bot.reply_to(message,"Enter valid command \n type /commands to list all commands")
#polling command to receive commands from bot
bot.infinity_polling()
