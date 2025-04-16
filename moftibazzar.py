import telebot
from telebot import types
import json
import os

TOKEN = "7784352743:AAHoG9jiGM5MwasfsbSjnBObApufKlfNBFg"
bot = telebot.TeleBot(TOKEN)

# دیتابیس ساده
USER_DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f)

user_data = load_data()

# کیبورد اصلی
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("ثبت سفارش 🛒", "پشتیبانی 📞")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
                   "لطفا گزینه مورد نظر را انتخاب کنید:",
                   reply_markup=main_keyboard())

# بخش سفارش
@bot.message_handler(func=lambda m: m.text == "ثبت سفارش 🛒")
def order(message):
    user_id = str(message.chat.id)
    user_data[user_id] = {"step": "نام سفارش"}
    save_data(user_data)
    
    msg = bot.send_message(message.chat.id,
                         "📝 لطفا نام و نام خانوادگی را وارد کنید:",
                         reply_markup=types.ForceReply())
    bot.register_next_step_handler(msg, get_phone_for_order)

def get_phone_for_order(message):
    user_id = str(message.chat.id)
    user_data[user_id]["نام"] = message.text
    user_data[user_id]["step"] = "شماره سفارش"
    save_data(user_data)
    
    msg = bot.send_message(message.chat.id,
                         "📱 لطفا شماره تماس را وارد کنید:",
                         reply_markup=types.ForceReply())
    bot.register_next_step_handler(msg, get_product_for_order)

def get_product_for_order(message):
    user_id = str(message.chat.id)
    user_data[user_id]["شماره"] = message.text
    user_data[user_id]["step"] = "محصول"
    save_data(user_data)
    
    msg = bot.send_message(message.chat.id,
                         "🛍️ لطفا کد و نوع محصول را وارد کنید:",
                         reply_markup=types.ForceReply())
    bot.register_next_step_handler(msg, finish_order)

def finish_order(message):
    user_id = str(message.chat.id)
    user_data[user_id]["محصول"] = message.text
    user_data[user_id]["step"] = None
    save_data(user_data)
    
    bot.send_message(message.chat.id,
                   f"✅ سفارش شما ثبت شد!\n"
                   f"نام: {user_data[user_id]['نام']}\n"
                   f"شماره: {user_data[user_id]['شماره']}\n"
                   f"محصول: {user_data[user_id]['محصول']}\n\n"
                   f"همکاران ما به زودی با شما تماس خواهند گرفت.",
                   reply_markup=main_keyboard())

# بخش پشتیبانی
@bot.message_handler(func=lambda m: m.text == "پشتیبانی 📞")
def support(message):
    user_id = str(message.chat.id)
    user_data[user_id] = {"step": "نام پشتیبانی"}
    save_data(user_data)
    
    msg = bot.send_message(message.chat.id,
                         "📝 لطفا نام و نام خانوادگی را وارد کنید:",
                         reply_markup=types.ForceReply())
    bot.register_next_step_handler(msg, get_phone_for_support)

def get_phone_for_support(message):
    user_id = str(message.chat.id)
    user_data[user_id]["نام"] = message.text
    user_data[user_id]["step"] = "شماره پشتیبانی"
    save_data(user_data)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ارسال پیام به پشتیبانی", url="https://t.me/pooshak_plase"))
    
    bot.send_message(message.chat.id,
                   f"✅ اطلاعات شما ثبت شد!\n"
                   f"نام: {user_data[user_id]['نام']}\n"
                   f"شماره: {user_data[user_id]['شماره']}\n\n"
                   f"لطفا برای ارتباط با پشتیبانی روی دکمه زیر کلیک کنید:",
                   reply_markup=markup)

if __name__ == '__main__':
    print("✅ ربات فعال شد...")
    bot.polling(none_stop=True)
