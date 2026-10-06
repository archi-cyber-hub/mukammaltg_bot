import os
import telebot
from telebot import types
import yt_dlp

# Botingizning Tokeni
TOKEN = "8812714505:AAEeYlQlUvU-ePMhmoc1rU3RaJyEaVHr_FI"
bot = telebot.TeleBot(TOKEN)

# /start komandasi uchun javob
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "tayyorman qani kettik:"
    )
    
    # Admin bilan bog'lanish uchun inline tugma
    markup = types.InlineKeyboardMarkup()
    admin_btn = types.InlineKeyboardButton("👨‍💻 Admin bilan bog'lanish", url="https://t.me/Anvarovahmadjon")
    markup.add(admin_btn)
    
    # Rasm va matnni birga yuborish
    try:
        with open('logo.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=markup)
    except FileNotFoundError:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Foydalanuvchi link yoki matn yuborganda ishlaydigan qism
@bot.message_handler(func=lambda message: True)
def handle_media(message):
    text = message.text.strip()
    
    # Agar xabar havolasi (link) bo'lsa yoki matn bo'lsa
    msg = bot.send_message(message.chat.id, "⏳ Qidirilmoqda va yuklab olinmoqda, iltimos biroz kuting...")
    
    try:
        # yt-dlp sozlamalari
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'max_filesize': 50 * 1024 * 1024, # Telegram cheklovi uchun 50MB gacha
        }
        
        # Agar bu matn bo'lsa (link bo'lmasa), YouTube'dan qidirish uchun so'rov tayyorlaymiz
        search_query = text
        if not text.startswith("http://") and not text.startswith("https://"):
            search_query = f"ytsearch1:{text}" # Eng birinchi chiqqan natijani oladi

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            
            # Agar qidiruv natijasi ro'yxat bo'lsa (ytsearch natijasi)
            if 'entries' in info:
                info = info['entries'][0]
                
            file_path = ydl.prepare_filename(info)
            
            # Videoni foydalanuvchiga yuborish
            with open(file_path, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption=f"🎬 Mana, siz so'ragan media: {info.get('title', 'Video')}")
            
            # Yuborib bo'lgach, serverni to'ldirmaslik uchun faylni o'chirib tashlaymiz
            if os.path.exists(file_path):
                os.remove(file_path)
                
            # Kutish xabarini o'chirib tashlaymiz
            bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik yuz berdi yoki video topilmadi.\n(Batafsil: {str(e)[:100]})", message.chat.id, msg.message_id)

# Botni 1 soniya tezlikda to'xtovsiz ishlab turishi uchun polling
if __name__ == '__main__':
    # Downloads papkasi yo'q bo'lsa, yaratib qo'yamiz
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    print("Bot ishga tushdi va buyruqlarni kutmoqda...")
    bot.infinity_polling(interval=1, timeout=20)
      
