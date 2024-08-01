import os
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive"

def run():
    app.run(host="0.0.0.0", port=os.getenv("PORT"))

def keep_alive():
    t = Thread(target=run)
    t.start()