import telebot
import yaml

with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']    
bot = telebot.TeleBot(token)

### FUNCTIONS ###
def send_message(message, response_text=None):
    bot.send_message(message.chat.id, response_text)
    
def main_func(message):
    text = str(message.text)
    return text if text != '' else None

### HANDLERS ###
@bot.message_handler(commands=["help"])
def help_processing(message):
    send_message(message, response_text='Помощь.')
    
@bot.message_handler(content_types=["text"])
def text_processing(message): 
    send_message(message, response_text=f'Обработка запроса.')
    result = main_func(message)
    if result:
        send_message(message, response_text=result)
    else:
        send_message(message, response_text=f'Ошибка.\n/help')

### MAIN ###        
def main():
    bot.infinity_polling()
    
if __name__ == '__main__':
    main()
    