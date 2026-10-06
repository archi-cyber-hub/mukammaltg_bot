import os
import threading
from flask import Flask
import telebot
from telebot import types
import yt_dlp

# Render port talabini qondirish uchun kichik veb-server
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Botingizning Tokeni
TOKEN = "8812714505:AAEeYlQ1UvU-ePMhmoc1rU3..."
bot = telebot.TeleBot(TOKEN)

# /start komandasi uchun javob
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "tayyorman qani kettik:"
    bot.send_message(message.chat.id, welcome_text)

if __name__ == '__main__':
    # Flask serverni alohida oqimda ishga tushiramiz
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Botni ishga tushiramiz
    bot.infinity_polling()
