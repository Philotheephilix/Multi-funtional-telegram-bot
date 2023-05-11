# Multi-funtional-telegram-bot
## Usage and need of this bot
This bot can automate these following tasks

  1. Convert photos to PDF: When the user sends the command "/jpg2pdf", the bot converts all the photos in the "tempimg" folder to PDFs and saves them in the "temppdf" folder. Then, the bot merges all the PDFs into a single PDF named "merged.pdf" and sends it to the user. Finally, the bot deletes all the temporary files.

  2. Check unread emails: When the user sends the command "/check_email", the bot logs in to the user's Gmail account, checks the number of unread emails in the inbox, and replies to the user with the number of unread emails.

  3. Tell a joke: When the user sends the command "/tell_joke", the bot reads a random joke from a text file named "joke.txt" and sends it to the user.

  4. Weather information: When the user sends the command "/weather", the bot asks the user to set the city. Then, when the user sends the city name, the bot retrieves the current weather information of the city from the OpenWeatherMap API and sends it to the user. If the weather is "broken clouds", the bot sends a photo of broken clouds to the user.

  5. Greeting: When the user sends the command "/start", the bot greets the user with "Hey! Hows it going?"

  6. SOS(Emergency Numbers): When the user sends the command "/sos ,the bot asks the user to set the country name. Then, when the user sends the country name, the bot retrieves the current SOS numbers for that country and returns it for example: if the user sets the country as "India" the bot returns 
        Emergency Numbers For India
        Ambulance = 102
        Fire = 101
        Police = 100

  7. Commands : This command returns all the available commands 

  8. Reels : When the user sends the command "/sos ,the bot asks the user to send instagram reel link, when the user sends the link the bot retrieves the reels video from instagram and sends it to the user
## Links
[Releases](https://github.com/Philotheephilix/Multi-funtional-telegram-bot/releases)


[Contributors](https://github.com/Philotheephilix/Multi-funtional-telegram-bot/graphs/contributors)

## Introduction
   This library provides a pure Python code for the Telegram Bot . It's completely made with Python 3

   Introducing a Python-based Telegram bot that is designed to simplify your messaging experience on the popular platform. This bot is built using the Telegram Bot API and can be easily installed and deployed on any machine that runs Python.

   This bot provides an easy-to-use interface that allows users to interact with the Telegram platform using a set of pre-defined commands. Whether you want to send messages, images, or documents, this bot has got you covered.

   The bot is designed with modularity in mind, meaning it is built using a set of self-contained modules that can be easily extended or modified to fit your specific use case. Some of the core modules used in the bot include the python-telegram-bot library for interacting with the Telegram Bot API, requests module for making HTTP requests, os module for working with the operating system
  
   Overall, this Telegram bot is a powerful and versatile tool that can help streamline your messaging experience on the platform. Its modular design make it a great choice for anyone looking to build custom solution for performing routine tasks with single click on Telegram.



## Installing
### 1. You need to create a telegram bot first follow steps given below to get started
BotFather is the official bot used to create and manage Telegram bots. Here are the steps to create a bot using BotFather:

      1.Open Telegram and search for BotFather in the search bar.
  
      2.Click on the BotFather and then click on the "Start" button.
  
      3.Type /newbot command to create a new bot.
  
      4.Give a name to your bot and choose a username for it. The username should end with "bot". For example, MyTestBot.
  
      5.BotFather will then give you an API token that you will use to communicate with your bot. Save this token somewhere safe as you will need it later.

      6. And also add these commands to the bot

              start - greet to check life of the bot
              tell_joke - returns a random joke
              weather - view the weather of the city
              check_email - check email for unread messages
              jpg2pdf - converts images to pdf
              sos - emergency contact number
              commands - list all commands
              reels - download instagram reels

  
  HOORAY Your bot is now created and ready to be configured.

2.Clone this repository on your local machine 

3.install these modules in python using pip 

	telebot
  
	pillow
  
	pypdf (version 2.0 as latest 3.0 has some issues)
    
	cryptography
  
	dotenv
    
	instagrapi
  
4. Configure email and API tokens 

5. Run Initialize.py script in Python IDLE or in some IDE first to configure all needed credentials 

6. Then, Run multi_bot.py to start the bot



## Security 
  Our goal is to provide secure environment so we have no unneccessary online communication like analytics it's just standalone on your desk

  As we give our E-Mail id to our bot we don't know how secure is this we are working on that to improvise the privacy.

  We have included environmental variable to store all the credentials which is encrypted while executing initialize.py and will be only decrypted during bot startup

  The most important thing is that it is based on rolling codes and the encryption key changes everytime you start the bot and is stored securely

## Feature request 
  If you guys are into some feature just feel free to contact me through  [TELEGRAM](https://t.me/philo_thee_philix)

## Disclaimer 
  Anyone can download or copy our code to use and redistribute but if you copy the whole code to someother projects kindly don't forget to give credits
