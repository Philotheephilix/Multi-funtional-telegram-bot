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
API_KEY = "6204099009:AAE-SAOmucAseVsMGHgron0A2OsTIKu3884"
bot = telebot.TeleBot(API_KEY)
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API = "533736d7bda8fe68d7914d84c0354da6"
bot = telebot.TeleBot(API_KEY)
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    file_name = 'temp/' + file.file_path.split('/')[-1]
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Photo saved!")
@bot.message_handler(commands=["jpg2pdf"])
def convert(message):
    dir=r'C:\Users\Administrator\Music\hackathon\temp'
    a=os.listdir(dir)
    for i in a:
        dirf=r'C:\Users\Administrator\Music\hackathon\temp'+"\\"+i
        dirsav=r'C:\Users\Administrator\Music\hackathon\temp'+i+".pdf"
        im=Image.open(dirf)
        imc=im.convert('RGB')
        imc.save(dirsav)
    pdfs_dir =r'C:\Users\Administrator\Music\hackathon'  
    merged_file_name = 'merged.pdf'
    pdf_merger = PdfFileMerger()
    for filename in os.listdir(pdfs_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdfs_dir, filename)
            with open(file_path, 'rb') as pdf_file:
                pdf_merger.append(pdf_file)
    with open(merged_file_name, 'wb') as merged_file:
        pdf_merger.write(merged_file)
    print('PDFs merged successfully!')
    with open("merged.pdf", 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file)
        bot.reply_to(message, "PDF file sent")
@bot.message_handler(commands=["check_email"])
def check_email(message):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    username = "philosanjaychamberline.26csb@licet.ac.in"
    password = "456@Icam"
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
@bot.message_handler(commands=["tell_joke"])
def tell_joke(message):
    i=random.randrange(0,1600)
    joke=open("joke.txt","r")
    data=joke.read().split(",") 
    data=remove(data)
    a=data[i]
    print(a)
    bot.reply_to(message, a)
@bot.message_handler(commands=["start"])
def greet(message):
    bot.reply_to(message,"Hey! Hows it going?")
@bot.message_handler(commands=["weather"])
def weather(message):
    bot.reply_to(message, "Set City")
@bot.message_handler(func=lambda m: True)
def city(message):
    if type(message.text) != "philo":
        global CITY
        CITY = str(message.text)
        print(CITY)
        url = BASE_URL + "appid=" + API + "&q=" + CITY
        response = requests.get(url).json()
        temp_kelvin = response["main"]['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response["main"]['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        print(description)
        if (description == 'broken clouds'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\brokenclouds.jpg', 'rb'))
        elif (description == 'few clouds'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\fewclouds.jpg', 'rb'))
        elif (description == 'overcast clouds'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\overcastclouds.jpg', 'rb'))
        elif (description == 'scattered clouds'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\scatteredclouds.jpg', 'rb'))
        elif (description == 'clearsky'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\clearsky.jpg', 'rb'))
        elif (description == 'mist'):
            bot.send_photo(chat_id=message.chat.id, photo=open(r'C:\Users\Administrator\Music\hackathon\img\mist.jpg', 'rb'))
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
bot.polling()
