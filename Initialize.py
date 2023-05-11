import os
from cryptography.fernet import Fernet
with open('crypt.key', 'wb') as filekey:
    filekey.write(key)
def init_var():
    mod={
        "E-mail_for_checking_email":"",
        "Password_for_checking_mail":"",
        "Instagram_username":"",
        "Instagram_password":"",
        "Telegram_bot_API":"",
        "Open_Weather_API":""
        }
    data=open("kets.env","r")
    dada=data.readlines()
    for val in dada:
        print(val)
        k,v=val.strip().split(":",1)
        if k in mod:
            new_value = input(f"Enter a new value for {k}: ")
            mod[k] = new_value
    data.close()
    data=open("kets.env","w")
    for key, value in mod.items():
        data.write(f"{key}:{value}\n")
    data.close()
    data=open("kets.env","r")
    dada=data.read()
    print(dada)
def encrypt():
    key = Fernet.generate_key()
    with open('crypt.key', 'wb') as filekey:
        filekey.write(key)
        print("new key gen")    
    with open('crypt.key', 'rb') as filekey:
        key = filekey.read()        
    fernet = Fernet(key)
    with open('kets.env', 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open('kets.env', 'wb+') as encrypted_file:
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
init_var()
encrypt()