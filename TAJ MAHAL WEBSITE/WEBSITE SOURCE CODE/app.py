from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image
import os
from flask import Flask, redirect, render_template, url_for,request,session,send_from_directory
import mysql.connector
import re
import wikipedia
from selenium import webdriver
import pyttsx3 
import pywhatkit
import speech_recognition as sr
from werkzeug.utils import secure_filename
import datetime





app = Flask(__name__)
app.secret_key = 'Bmthulas1'
app.config['UPLOAD_FOLDER'] = 'env/static/pictures/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']


con = mysql.connector.connect(host="localhost",user="root",password="Bmthulasi1@",database="website")
web =con.cursor(dictionary=True)

@app.route("/",methods=['GET','POST'])
def home():
    msg = ""
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            sql = 'SELECT * FROM user_details WHERE USERNAME = %s AND PASSWORD = %s'
            web.execute(sql,[username,password])
            res = web.fetchone()
            if res:
                session['loggedin'] = True
                session['ID'] = res['ID']
                session['USERNAME'] = res['USERNAME']
                msg = 'Logged in successfully !'
                speaker = pyttsx3.init()
                speaker.say(username+"hai welcome.... to this website .......happy to meet you")
                speaker.runAndWait()
                return redirect('my account')
            else:
                msg = "invalid username and password try again later"
                return redirect('login')   
    return render_template("website.html",msg = msg)    
@app.route("/history")
def history():
    return render_template("history.html")
@app.route("/login",methods=['GET','POST'])
def login():
    msg = ""
    if request.method == 'POST':
            username = request.form['username']
            gmail = request.form['gmail']
            password = request.form['password']
            role = request.form['role']
            about = request.form['about']
            sql = 'SELECT * FROM user_details WHERE USERNAME = %s AND GMAIL = %s AND PASSWORD = %s AND ROLE = %s AND ABOUT = %s'
            web.execute(sql,[username,gmail,password,role,about])
            res = web.fetchone()
            if res:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', gmail):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not gmail:
                msg = 'Please fill out the form !'
            else:
                sql = "INSERT INTO user_details(USERNAME,GMAIL,PASSWORD,ROLE,ABOUT)values(%s,%s,%s,%s,%s)"
                web.execute(sql,[username,gmail,password,role,about])
                con.commit()
                return redirect('login')
    return render_template("login.html",msg = msg)
@app.route("/my account",methods=['POST','GET'])
def account():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files != "":
        msg = "PLEASE REMOVE YOUR OLD PROFILE"
    print(files)
    for image in files:
        extension = os.path.splitext(image)[1].lower()
        if extension in app.config['ALLOWED_EXTENSIONS']:
            print(extension)
    sql="SELECT * FROM user_details"
    web.execute(sql)
    res=web.fetchall()
    con.commit()
    return render_template("account.html",datas=res,files=files,msg=msg)

@app.route("/delete/<id>",methods = ['GET','POST'])
def logout(id):
    web.execute("DELETE FROM user_details WHERE id=%s",[id])
    con.commit()
    return redirect(url_for('account'))

@app.route("/upload",methods=['POST','GET'])
def upload():
    try:
       picture = request.files['picture']
       extension = os.path.splitext(picture.filename)[1].lower()


       if picture:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return('File is not an image.')

            new_size = Image.open(picture)
            image = new_size.resize((100,100))

            print(new_size.size)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(picture.filename)))

    except RequestEntityTooLarge: 
        return ("File is larger than the 16MB limit")
    return redirect(url_for('account'))

@app.route("/shajahan")
def shajahan():
    return render_template("shajahan.html")

@app.route("/assistant")
def assistant():
    sql = "SELECT * FROM voice"
    web.execute(sql)
    result = web.fetchall()
    return render_template("vr.html",datas=result)

@app.route("/Remove")
def Remove():
    web.execute("DELETE FROM voice")
    con.commit()
    return redirect(url_for("assistant"))
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        box = request.form["google"]
        print(box)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        browser = webdriver.Chrome("env/chromedriver.exe",options=options)
        search = browser.get("https://www.google.com/search?q=" + box + "&start" +str(box))
        return redirect(url_for("assistant"))
@app.route("/search with mic")
def search1():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        speech = listener.listen(source)
        command = listener.recognize_google(speech)
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        browser = webdriver.Chrome("env/chromedriver.exe",chrome_options=option)
        for i in range(1):
            element = browser.get("https://www.google.com/search?q=" + command + "&start" + str(i))
    return redirect(url_for("assistant"))
@app.route("/sofia")
def sofia():
    listener = sr.Recognizer()
    COMMAND = ""
    HELLO = ""
    with sr.Microphone() as source:
        voice = listener.listen(source)
        COMMAND = listener.recognize_google(voice)
        COMMAND = COMMAND.lower()
        print()
        print(COMMAND)
        if "hello sofia" in COMMAND:
            HELLO = "Hello i am listening.How can i  help you today? 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif COMMAND == "sofia":
            HELLO = "Hello i am here with you.how do you today? 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("Hello i am here with you.How do you today?")
            speaker.runAndWait()
        elif "bye" in COMMAND:
            HELLO = "Mmmm bye see you later 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("Mmmm bye see you later")
            speaker.runAndWait()
        elif COMMAND == "i am fine":
            HELLO = "hmmm. ok. that's. good 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("hmmm ok that's good")
            speaker.runAndWait()
        elif "fine" in COMMAND:
            HELLO = "hmmm ok that's nice have a nice day 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("hmmm ok that's nice have a nice day")
            speaker.runAndWait()
        elif COMMAND == "hello":
            HELLO = "hmmm. oh hello i am sofia good to see you how are you 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("hmmm. oh hello i am sofia good to see you how are you")
            speaker.runAndWait()
        elif "know" in COMMAND:
            HELLO = "sorry don't know about that"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("sorry don't know about that that")
            speaker.runAndWait()
        elif  "are you single" in COMMAND:
            HELLO = "no i had relationship with wifi 💗"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("no i had relationship with wifi")
            speaker.runAndWait()
        elif "married " in COMMAND:
            HELLO = "yes i married my boss 🌹"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("yes i married my boss ")
            speaker.runAndWait()
        elif "say" and "about" in COMMAND:
            HELLO = wikipedia.summary(COMMAND, sentences = 2)
        elif "talk" and "about" in COMMAND:
            HELLO = wikipedia.summary(COMMAND,sentences = 2)
        elif "tell" and "about" in COMMAND:
            HELLO = wikipedia.summary(COMMAND,sentences = 2)
        elif "speak" and "about" in COMMAND:
            HELLO = wikipedia.summary(COMMAND,sentences = 2)
        elif "what do you about" in COMMAND:
            HELLO = wikipedia.summary(COMMAND,sentences = 2)
        elif "know about sofia" in COMMAND:
            HELLO = "hmmm she is voice assistant,she is a good assistant for you 😄"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say("hmmm she is voice assistant,she is a good assistant for you")
            speaker.runAndWait()
        elif "good morning" in COMMAND:
            current_time = datetime.datetime.now().strftime("%H:%M:%p")
            print(current_time)
            current_time = str(current_time)
            if current_time >= "05:00:AM" and current_time <= "12:00:PM":
                HELLO =  "good morning 🌞" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("good morning")
                speaker.runAndWait() 
            elif current_time >= "12:00:PM" and current_time <= "17:00:PM":
                HELLO = "sorry this is good afternoon 😠" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good afternoon")
                speaker.runAndWait()
            elif current_time >= "17:00:PM" and current_time <= "19:00:PM":
                HELLO =  "sorry this is good evening 😠" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good evening")
                speaker.runAndWait()
            elif current_time >= "19:00:PM" and current_time <= "24:00:PM":
                HELLO =  "sorry this is good night 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good night")
                speaker.runAndWait()
        elif "good afternoon" in COMMAND:
            current_time = datetime.datetime.now().strftime("%H:%M:%p")
            print(current_time)
            current_time = str(current_time)
            if current_time >= "05:00:AM" and current_time <= "12:00:PM":
                HELLO =  "sorry this is good morning 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good morning")
                speaker.runAndWait() 
            elif current_time >= "12:00:PM" and current_time <= "17:00:PM":
                HELLO = "hmm ok good afternoon 😄 " + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("hmm ok good afternoon ")
                speaker.runAndWait()
                print(type(current_time))
            elif current_time >= "17:00:PM" and current_time <= "19:00:PM":
                HELLO =  "sorry this is good evening 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good evening ")
                speaker.runAndWait() 
            elif current_time >= "19:00:PM" and current_time <= "24:00:PM":
                HELLO =  "sorry this is good night 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good night")
                speaker.runAndWait()
        elif "good evening" in COMMAND:
            current_time = datetime.datetime.now().strftime("%H:%M:%p")
            print(current_time)
            current_time = str(current_time)
            if current_time >= "05:00:AM" and current_time <= "12:00:PM":
                HELLO =  "sorry this is good morning 😠" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good morning")
                speaker.runAndWait()
            elif current_time >= "12:00:PM" and current_time <= "17:00:PM":
                HELLO = "sorry this is good afternoon 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good afternoon")
                speaker.runAndWait() 
                print(type(current_time))
            elif current_time >= "17:00:PM" and current_time <= "19:00:PM":
                HELLO =  "hmm ok good evening 😄" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("hmm ok good evening")
                speaker.runAndWait()
            elif current_time >= "19:00:PM" and current_time <= "24:00:PM":
                HELLO =  "sorry this is good night 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good night")
                speaker.runAndWait()
        elif "good night" in COMMAND:
            current_time = datetime.datetime.now().strftime("%H:%M:%p")
            print(current_time)
            current_time = str(current_time)
            if current_time >= "05:00:AM" and current_time <= "12:00:PM":
                HELLO =  "sorry this is good morning 😠" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good morning")
                speaker.runAndWait()
            elif current_time >= "12:00:PM" and current_time <= "17:00:PM":
                HELLO = "sorry this is good afternoon 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good afternoon")
                speaker.runAndWait() 
            elif current_time >= "17:00:PM" and current_time <= "19:00:PM":
                HELLO =  "sorry this is good evening 😠" + current_time
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("sorry this is good evening sweet dreams")
                speaker.runAndWait() 
            elif current_time >= "19:00:PM" and current_time <= "24:00:PM":
                HELLO =  "hmm good night 😴" + current_time 
                speaker = pyttsx3.init()
                voices = speaker.getProperty("voices")
                speaker.setProperty("voice",voices[1].id)
                speaker.say("hmm good night")
                speaker.runAndWait()
        elif "are you married" in COMMAND:
            HELLO = "hmm i married my boss 😍"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif "time" in COMMAND:
            time = datetime.datetime.now().strftime("%H : %M : %p")
            HELLO = ("CURRENT TIME IS 🕙" +time)
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
            print(HELLO)
        elif  "are you crazy" in COMMAND:
            HELLO = "i am not crazy you are crazy "
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif  "are you made" in COMMAND:
            HELLO = "i am not mad you are mad "
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif "how are you" in COMMAND:
            HELLO = "i am fine thanks for asking  this ❤️"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
            print(HELLO)
        elif "+" in COMMAND:
            res = []
            for i in COMMAND.split():
                if i.isdigit():
                    res.append(i)
            print(res)
            a = res[0]
            a = int(a)
            b = res[1]
            b = int(b)
            g = a + b
            g = str(g)
            print(g)
            HELLO = "your answer is 👍" +g
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(g)
            speaker.runAndWait()
        elif "-" in COMMAND:
            res = []
            for i in COMMAND.split():
                if i.isdigit():
                    res.append(i)
            print(res)
            a = res[0]
            a = int(a)
            b = res[1]
            b = int(b)
            g = a - b
            g = str(g)
            print(g)
            HELLO = "your answer is 🤔:" +g
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(g)
            speaker.runAndWait()
        elif "multiple" in COMMAND:
            res = []
            for i in COMMAND.split():
                if i.isdigit():
                    res.append(i)
            print(res)
            a = res[0]
            a = int(a)
            b = res[1]
            b = int(b)
            g = a * b
            g = str(g)
            print(g)
            HELLO = "your answer is 🤔:" +g
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(g)
            speaker.runAndWait()
        elif "divided" in COMMAND:
            res = []
            for i in COMMAND.split():
                if i.isdigit():
                    res.append(i)
            print(res)
            a = res[0]
            a = int(a)
            b = res[1]
            b = int(b)
            g = a / b
            g = str(g)
            print(g)
            HELLO = "your answer is 🤔" +g
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(g)
            speaker.runAndWait()
        elif "status" in COMMAND:
            status = COMMAND.replace("playing" ,"")
            pywhatkit.playonyt(status)
            HELLO = " 🎼 "+status
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif "song" in COMMAND:
            song = COMMAND.replace("playing song","")
            pywhatkit.playonyt(song)
            HELLO = "💃"+song
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO)
            speaker.runAndWait()
        elif "movie" in COMMAND:
            movie = COMMAND.replace("playing movie","")
            pywhatkit.playonyt(movie)
            HELLO = "I am  go to ask youtube uncle."
            HELLO1 = "I. am. go. to. ask. youtube. uncle"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO1)
            speaker.runAndWait()
        elif "movies" in COMMAND:
            movies = COMMAND.replace("playing movies","")
            pywhatkit.playonyt(movies)
            HELLO = "I AM GO TO REFFER YOUTUBE"
            HELLO1 = "I.. am.. go.. to.. reffer.. youtube.. "
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO1)
            speaker.runAndWait()
        elif "search" in COMMAND:
            HELLO = "hello i am there for your kindly request.please enter your searching word here"
            speaker = pyttsx3.init()
            voices = speaker.getProperty("voices")
            speaker.setProperty("voice",voices[1].id)
            speaker.say(HELLO1)
            speaker.runAndWait()
        elif "taj mahal " and "history" in COMMAND:
            HELLO = "i will show you here"
            return redirect(url_for("history"))
        elif "mumtaj" and "history" in COMMAND:
            HELLO = "i will it for you here "
            return redirect(url_for("mumtaj"))
        elif "shajahan " and "history" in COMMAND:
            HELLO = "hmmm ok "
            return redirect(url_for("shajahan"))
        elif "structure" and "design" in COMMAND:
            HELLO = "hmmm yes i will reffer it for you"
            return redirect(url_for("design"))
        elif "stucture" in COMMAND:
            HELLO = "hmmm thanks for asking this"
            return redirect(url_for("design"))
        elif  "design" in COMMAND:
            HELLO = "hmmm this is for your kindly request"
            return redirect(url_for("design"))
        elif "login" in COMMAND:
            HELLO = "hmmm i will return it"
            return redirect(url_for("login"))
        elif "sign up" in COMMAND:
            HELLO = "hmmm thanks for asking this"
            return redirect(url_for("login"))
        elif "home" in COMMAND:
            HELLO = "hmmm yeah"
            return redirect(url_for("home"))
        elif "account" in COMMAND:
            HELLO = "hmmm i will for asking this"
            return redirect(url_for("account"))
        elif "log out" in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("account"))
        elif "log out" and "my account" in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("account"))
        elif "sofia" in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("assistant"))
        elif "my sofia" in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("assistant"))
        elif "voice assistant " in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("assistant"))
        elif "virtual assistant " in COMMAND:
            HELLO = "hmmm i will do this for you"
            return redirect(url_for("assistant"))
        elif COMMAND == "what do you know about taj mahal":
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif COMMAND == "what is taj mahal":
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "taj mahal" in COMMAND:
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "talk" and "taj mahal" in COMMAND:
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "tell" and "taj mahal" in COMMAND:
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "say" and "taj mahal" in COMMAND:
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "speak" and "taj mahal" in COMMAND:
            HELLO = "The Taj Mahal is an Islamic religious building, mosque and tomb in India, built in the 17th century by Emperor Shah Jahan in memory of his wife, Mumtaz Mahal. Its chief architect was Ustad Ahmad Lahauri.The building is in the city of Agra, Uttar Pradesh. Widely thought as one of the most beautiful buildings in the world, it is one of India's biggest tourist attractions.It is listed as a UNESCO World Heritage Site, together with the Agra Fort, 2.5 kilometers away, and was listed as one of the 7 Wonders of the World in 2007. It is located on the south bank of Yamuna river in Agra."
        elif "tell" and "taj mahal story" in COMMAND:
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        elif "speak" and "taj mahal story" in COMMAND:
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        elif "talk" and "taj mahal story" in COMMAND:
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        elif "say" and "taj mahal story" in COMMAND:
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        elif "taj mahal" and "story" in COMMAND:
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        elif COMMAND == "taj mahal story":
            HELLO = "It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD, with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters were added subsequently and completed in 1653 AD."
        else:
            HELLO = "i am searching google"  + COMMAND
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach",True)
            browser = webdriver.Chrome("env/chromedriver.exe",options=options)
            for i in range(1):
                search = browser.get("https://www.google.com/search?q=" + COMMAND + "&start" )
        web = con.cursor(dictionary=True)
        sql = "INSERT INTO voice(COMMAND,HELLO)values(%s,%s)"
        web.execute(sql,[COMMAND,HELLO])
        result = web.fetchall()
        con.commit()

        sql = "SELECT * FROM voice"
        web.execute(sql)
        result = web.fetchall()
        return render_template("vr.html",datas = result)
@app.route("/mumtaj")
def mumtaj():
    return render_template("mumtaj.html")

@app.route("/design")
def design():
    return render_template("design.html")

@app.route('//<filename>',methods=['GET'])
def upload_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete-image/<photo>',methods=['GET','POST'])
def delete(photo):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],photo))
        return redirect(url_for('account'))

@app.route("/text")
def text():
    speaker = pyttsx3.init()
    speaker.say("It was built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal with construction starting in 1632 AD and completed in 1648 AD with the mosque, the guest house and the main gateway on the south, the outer courtyard and its cloisters.. were.. added.. subsequently and completed in 1653 AD.The Taj Mahal is considered one of the worlds seven wonders.Taj Mahal was built in about 17th century.Shah Jahan, the Mughal Emperor, built it.He built it in the memory of his beloved wife")
    speaker.runAndWait()
    return redirect(url_for("history"))
@app.route("/thanks")
def thanks():
    speaker = pyttsx3.init()
    speaker.say("Ok..Thank..you")
    speaker.runAndWait()
    return redirect(url_for("history"))
@app.route("/text1")
def text1():
    speaker = pyttsx3.init()
    speaker.say("The Taj Mahal is considered one of the world's seven wonders.Taj Mahal was built in about 17th century.Shah Jahan, the Mughal Emperor, built it.He built it in the memory of his beloved wife.There is one mosque around the Taj Mahal.It has four stunning minars that add to its charm.")
    speaker.runAndWait()
    return redirect(url_for('home'))

if __name__ in "__main__":
  app.run(debug=True)
