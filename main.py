import hashlib
import json
from random import randint
import smtplib
import ssl
from email.message import EmailMessage
import re
from os import listdir
from os.path import isfile, join
import os

def mailcode(receiver,code):
    #specify details
    email_sender = 'adamtestpython@gmail.com'
    email_password = 'jzojeebududlirnk'
    email_receiver = receiver
    subject = 'verification code'
    body = """
    here is your verification code::
    """ + str(code)
    
    #build the email
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    #send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def checkPasswordStrenght(password):
    conditionsFulfilled = 0
    if re.search("[A-Z]", password): #contains an upper case
        conditionsFulfilled += 1
    if re.search("[a-z]", password): #contains a lower case
        conditionsFulfilled += 1
    if re.search("[0-9]", password): #contains a number
        conditionsFulfilled += 1
    if re.search("[^A-Za-z0-9]", password): #contains a special character
        conditionsFulfilled += 1

    if len(password) > 8 and conditionsFulfilled > 3:
        return True
    return False


def inputHash(prompt,check):
    inputtedString = input(prompt)
    hashedInputtedString = hashlib.sha256(inputtedString.encode()).hexdigest()

    if check:
        isStrong = checkPasswordStrenght(inputtedString)
        return(hashedInputtedString,isStrong)

    return(hashedInputtedString)

def changePass(username):
    password,good = inputHash(language["new_pass"], True)

    while not good:
        print(language["pass_not_strong_enough"])
        password,good = inputHash("new password: ", True)

    repeated = inputHash(language["repeat_pass"], False)

    if password == repeated:
        data[username][0]=password
        print(language["pass_changed"])
    else:
        print(language["different_pass"])

def onLogin(username):

    print(language["login_statement"])

    #offer the user the option to change their password
    print(language["change_pass_question"])
    if input("(y/n): ") == "y":
        changePass(username)
        
def checkMailThruCode(usermail):
    #generate random verification code
    randomcode = randint(100000,999999)
    
    #send the code to the user
    mailcode(usermail,randomcode)

    incode = input(language["code_sent"].format(usermail))

    #verify the code
    if incode == str(randomcode):
        return True
        
    else:
        print(language["code_wrong"])
        return False

def resetPass(username):
    #get users email adress
    usermail = input(language["email"])
    
    #check if the email address is correct
    while not (hashlib.sha256(usermail.encode()).hexdigest() == data[username][1]):
        print(language["email_wrong"])
        usermail = input(language["email"])

    #send a code and reset users password
    if checkMailThruCode(usermail):
        changePass(username)

def login(username):
    while True:
        #get the password
        password = inputHash(language["pass"], False)

        #check the password
        if data[username][0] == password:
            onLogin(username)
            break

        else:
            print(language["pass_wrong"])

            #reset the password
            if input("y/n: ") == "y":
                resetPass(username)
            break

def createAccount(username):
    #get the email address from the user
    usermail = input(language["email"])

    #simple check for invalid input
    while not ("@" in usermail):
        print(language["email_wrong"])
        usermail = input(language["email"])

    #send a verification code to the user
    if checkMailThruCode(usermail):
        hashedEmail = hashlib.sha256(usermail.encode()).hexdigest()
        #create new entry in the JSON with user mail
        data[username] = ["",hashedEmail]
        #create new password
        changePass(username)
        print(language["account_created"])



#load the json account storage
with open("data.json","r") as file:
    data = json.load(file)

while True:
    print("language")
    cwd = os.getcwd()
    #get all the possible language files from "/languages"
    possibleLanguages = [f.split(".")[0] for f in listdir(cwd+"/languages") if isfile(join(cwd+"/languages", f))]
    selectedLanguage = input("/".join(possibleLanguages) + ": ")
    if selectedLanguage in possibleLanguages:
        break
    print("that language does not exist")

    



with open("languages/{}.json".format(selectedLanguage),"r",encoding="UTF-8") as file:
    language = json.load(file)


#get the username
username = input(language["username"])

#check if the username exists
if username in data:
    #username exists
    login(username)
         
else:
    #username does not exist
    print(language["username_doesnt_exist"])
    if input("y/n: ") == "y":
        createAccount(username)

        
        
#write changes to data.json
with open("data.json", "w") as outfile:
    json.dump(data, outfile)

input("press enter to continue")