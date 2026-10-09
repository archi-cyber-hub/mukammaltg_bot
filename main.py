import os
import telebot
import yt_dlp

TOKEN = "8812714505:AAHoa4KDxcfaAPw4_jnQTktIjheemr_8Wo4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "Salom! Men universal botman. 🚀\n"
        "Menga Instagram yoki YouTube'dan video havolasini tashlang, men uni sizga yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    # Havola ekanligini oddiy tekshirish
    if "http://" in url or "https://" in url:
        msg = bot.send_message(message.chat.id, "⏳ Video yuklab olinmoqda, biroz kuting...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        
        try:
            # Avvalgi yuklangan video bo'lsa o'chiramiz
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            if os.path.exists('video.mp4'):
                with open('video.mp4', 'rb') as vid:
                    bot.send_video(message.chat.id, vid, caption="Mana siz so'ragan video! 📥")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Videoni yuklab bo'lmadi.", message.chat.id, msg.message_id)
                
        except Exception as e:
            bot.edit_message_text(f"❌ Xatolik yuz berdi: {str(e)[:100]}", message.chat.id, msg.message_id)
    else:
        bot.send_message(message.chat.id, "Iltimos, to'g'ri video havolasini yuboring (masalan, Instagram yoki YouTube linki).")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()
