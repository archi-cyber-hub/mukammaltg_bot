import os
import telebot

TOKEN = "8812714505:AAHoa4KDxcfaAPw4_jnQTktIjheemr_8Wo4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Salom! Bot ishlayapti! 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Siz yozdingiz: {message.text}")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()
