import os
from cryptography.fernet import Fernet
To_be_written=[]
mod=["E-mail_for_checking_email","Password_for_checking_mail","Telegram_bot_API","Open_Weather_API"]
def init():
    mod=["E-mail_for_checking_email","Password_for_checking_mail","Telegram_bot_API","Open_Weather_API"]
    for i in range(len(mod)):
        new_value = input("Enter a new value for "+mod[i])
        To_be_written.append(new_value)
    data=open(".env","w")
    for i in range(len(mod)):
        data.write(mod[i]+"="+To_be_written[i]+"\n")
    data.close()
def encrypt():
    key = Fernet.generate_key()
    with open('crypt.key', 'wb') as filekey:
        filekey.write(key)
        print("new key gen")    
    with open('crypt.key', 'rb') as filekey:
        key = filekey.read()        
    fernet = Fernet(key)
    with open('.env', 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open('.env', 'wb+') as encrypted_file:
        encrypted_file.write(encrypted)
        enc=encrypted_file.read()
        print(enc)
def decrypt():
    try:
        with open('crypt.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open('.env', 'rb') as file:
            original = file.read()
        decrypted = fernet.decrypt(original)
        with open('.env', 'wb+') as decrypted_file:
            decrypted_file.write(decrypted)
            print("decrypted")
    except:
        print("Invalid Key or Already decrypted")
decrypt()
init()
encrypt()