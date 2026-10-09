import os
import threading
from flask import Flask
import telebot
import yt_dlp

# Render port talabini qondirish uchun veb-server
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

# /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Salom! Men universal media yuklab beruvchi botman.\n\n"
        "Menga Instagram yoki YouTube havolasini yuboring, men sizga videoni yuboraman!"
    )
    bot.send_message(message.chat.id, welcome_text)

# Havolalarni qabul qilib video yuklash
@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.send_message(message.chat.id, "Iltimos, to'g'ri havola (link) yuboring!")
        return

    msg = bot.send_message(message.chat.id, "⏳ Video yuklab olinmoqda, biroz kuting...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists("video.mp4"):
            with open("video.mp4", 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption="Mana siz so'ragan video! 🚀")
            bot.delete_message(message.chat.id, msg.message_id)
            os.remove("video.mp4")
        else:
            bot.edit_message_text("Kechirasiz, videoni yuklab bo'lmadi.", message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"Xatolik yuz berdi: {str(e)[:100]}", message.chat.id, msg.message_id)
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    bot.infinity_polling()