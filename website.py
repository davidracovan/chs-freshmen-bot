from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='https://chs-freshmen-bot.herokuapp.com/')

def start():
    t = Thread(target=run)
    t.start()