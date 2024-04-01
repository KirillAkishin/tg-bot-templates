import telebot
bot = telebot.TeleBot('xxx:YYYYYY')

@bot.message_handler(regexp='.*')
def text_processing(message): 
    bot.send_message(message.chat.id, 'Hello!')

if __name__ == '__main__':
    bot.infinity_polling()
    