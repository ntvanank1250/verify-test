import requests
import telebot
# Khởi tạo bot với access token
bot = telebot.TeleBot('6633842825:AAHhFb2CJCfWzTAdJoYI2mosSL6cjtQNzGA')
chat_id = -4054523942
# Gửi tin nhắn từ bot
def send_message(chat_id, message):
    bot.send_message(chat_id, message)