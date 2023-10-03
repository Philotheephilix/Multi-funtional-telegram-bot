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
import shutil
#
#
# INITIALIZE ALL REQUIRED KEYS AND CREDENTIALS BELOW FOR PROPER WORKING OF BOT
#
#
from cryptography.fernet import Fernet
#Variable initializing

is_weather="0"
sos_active="0"
emailinit_active=0
email_pass="0"
string=" "
cl = Client()
tempdir=os.getcwd()
Credentials={}
bot = ""
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
path=os.getcwd()
#Code for handling credential encryption and decryption
def encryptcred(msgid):
    key = Fernet.generate_key()
    with open('./credentials/'+msgid+'/crypt_cred.key', 'wb') as filekey:
        filekey.write(key)
        print("new key gen")    
    with open('./credentials/'+msgid+'/crypt_cred.key', 'rb') as filekey:
        key = filekey.read()        
    fernet = Fernet(key)
    with open("./credentials/"+msgid+'/credential.env', 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open("./credentials/"+msgid+'/credential.env', 'wb+') as encrypted_file:
        encrypted_file.write(encrypted)
        enc=encrypted_file.read()
        print(enc)
def decryptcred(msgid):
    try:
        with open('./credentials/'+msgid+'/crypt_cred.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open('./credentials/'+msgid+'/credential.env', 'rb') as file:
            original = file.read()
        decrypted = fernet.decrypt(original)
        with open('./credentials/'+msgid+'/credential.env', 'wb+') as decrypted_file:
            decrypted_file.write(decrypted)
            print("decrypted")
    except:
        print("Invalid Key or Already decrypted")
def decrypt():
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
decrypt()

#loading credentials and keys from env file

load_dotenv(tempdir+"\.env")       
TELE_API_KEY = os.getenv("Telegram_bot_API")
print(TELE_API_KEY)
OW_API = os.getenv("Open_Weather_API")
def encrypt():
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
encrypt()

# Directory creation and verification
def init_dirs():
    req_dir=("credentials","reels","temppdf","merged","tempimg")
    try:
        for i in req_dir:
            os.mkdir(path+"\\"+i)
            print("required dirs created")
    except FileExistsError:
        print("dirs already exists")
init_dirs()
#Bot initialization
def bot_init():
    global bot
    bot = telebot.TeleBot(TELE_API_KEY)
    bot = telebot.TeleBot(TELE_API_KEY)
bot_init()
# Initialize Joke.txt Dataset
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list
#Code for file handling (jpg2pdf) 
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    msgid=str(message.chat.id)
    try:
        os.mkdir(path+"\\tempimg\\"+msgid+"\\")
        os.mkdir(path+"\\temppdf\\"+msgid+"\\")
        os.mkdir(path+"\\merged\\"+msgid+"\\")
    except:
        print("folder exists")
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    print(file.file_path)
    file_name = 'tempimg/'+msgid + "/"+file.file_path.split('/')[-1]
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Photo saved!")
    print ("img in temp..")
#Code  for handling /commands
@bot.message_handler(commands=["commands"])
def message(message):
    bot_action=open("bot_action.txt","r")
    commands=bot_action.read()
    bot.reply_to(message,"Here are the list of commands \n"+commands)
#Code to handle jpg2pdf conversion
@bot.message_handler(commands=["jpg2pdf"])
def convert(message):
    msgid=str(message.chat.id)
    dir=tempdir+"\\tempimg\\"+msgid+"\\"
    a=os.listdir(dir)
    print(a)
    for i in a:
        dirf=tempdir+"\\tempimg\\"+msgid+"\\"+i
        dirsav=tempdir+"\\temppdf\\"+msgid+"\\"+i+".pdf"
        im=Image.open(dirf)
        imc=im.convert('RGB')
        imc.save(dirsav)
    pdfs_dir =tempdir+"\\temppdf\\"+msgid+"\\"
    merged_file_name = 'merged\\'+msgid+'\\merged.pdf'
    pdf_merger = PdfFileMerger()
    for filename in os.listdir(pdfs_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdfs_dir, filename)
            with open(file_path, 'rb') as pdf_file:
                pdf_merger.append(pdf_file)
    with open(merged_file_name, 'wb') as merged_file:
        pdf_merger.write(merged_file)
    print('PDFs merged successfully!')
    with open("merged\\"+msgid+"\\merged.pdf", 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file)
        bot.reply_to(message, "PDF file sent")
    def junk_removal():
        os.remove("merged\\"+msgid+"\\merged.pdf")
        print("merged pdf deleted....")
        for i in a:
            os.remove("tempimg\\"+msgid+"\\"+i)
        print("temp img is deleted")
        for i in a:
            os.remove("temppdf\\"+msgid+"\\"+i+".pdf")
        print("temp pdf is deleted..")
    junk_removal()
#Code to handle /check_email command
@bot.message_handler(commands=['init_email'])
def init_email(message):
    msgid=str(message.chat.id)
    global emailinit_active
    emailinit_active=1
    bot.reply_to(message,"Enter your email address")
    try:
        os.mkdir(path+"\\credentials\\"+msgid)
    except:
        print("Using previous directory")
    shutil.copy("./credential.env","./credentials/"+msgid+"/credential.env")
    shutil.copy("./crypt_cred.key","./credentials/"+msgid+"/crypt_cred.key")
@bot.message_handler(commands=["check_email"])
def check_email(message):
    msgid = str(message.chat.id)
    decryptcred(msgid)
    credential_path = os.path.join(tempdir, "credentials", msgid, "credential.env")
    
    # Read the email and password directly from the credential file
    with open(credential_path, "r") as credential_file:
        lines = credential_file.readlines()
        email = None
        password = None
        for line in lines:
            if line.startswith("email="):
                email = line.strip("email=").strip()
            elif line.startswith("pass="):
                password = line.strip("pass=").strip()
        if email and password:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email, password)
            mail.select("inbox")
            result, data = mail.search(None, "UNSEEN")
            unread_count = len(data[0].split())
            bot.reply_to(message, f"You have {unread_count} unread emails.")
            mail.logout()
        else:
            bot.reply_to(message, "Email and/or password not found in credentials.")
    encryptcred(msgid)
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
@bot.message_handler(commands=["weather","sos"])
def weather(message):
    status=str(message.text)
    print(status)
    global sos_active
    global is_weather
    if  status=="/weather":
        is_weather="1"
        bot.reply_to(message, "Set City")
    elif status=="/sos":
        sos_active="1"
        bot.reply_to(message,"Enter Country Name")
    else:
        pass  
#Code to handle execution of weather , sos, reels  
@bot.message_handler(func=lambda m: True)
def city(message):
    global is_weather
    global sos_active
    global emailinit_active
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
            print(message.chat.id)
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
    elif emailinit_active ==1 or emailinit_active==2:
        emailid=str(message.text)
        msgid=str(message.chat.id)
        decryptcred(msgid)


        newline="\n"        
        newline=newline.encode()
        Credential=open("./credentials/"+msgid+"/credential.env","ab")
        if emailinit_active==1:
            emailid="email="+emailid
            emailid=emailid.encode()
            Credential.write(emailid)
        else:
            emailid="pass="+emailid
            emailid=emailid.encode()
            Credential.write(emailid)
        Credential.write(newline)
        emailinit_active+=1
        if emailinit_active<=2:
            bot.send_message(message.chat.id,"Enter your email password")   
        else:
            emailinit_active=0
            Credential=open("./credentials/"+msgid+"/credential.env","r")
            cred=Credential.read()
            bot.send_message(message.chat.id,"verify ur credentials\n"+cred)
            encryptcred(msgid)

    
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
