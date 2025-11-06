import logging
logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    format='%(asctime)-17s | %(levelname)-8s | %(message)s', 
    datefmt='%y-%m-%d %H:%M:%S',
    level=logging.INFO)
import yaml
with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  
import telebot
bot = telebot.TeleBot(token)

### FUNCTIONS ###
def main_func(message):
    text = str(message.text)
    return text if text != '' else None

def send_message(message, response_text=None):
    logging.info('/help')
    bot.send_message(message.chat.id, response_text)

### HANDLERS ###
@bot.message_handler(commands=["help"])
def help_processing(message):
    logging.warning('/help')
    send_message(message, response_text='Помощь.')
    
@bot.message_handler(content_types=["text"])
def text_processing(message): 
    send_message(message, response_text='Обработка запроса.')
    result = main_func(message)
    if result:
        send_message(message, response_text=result)
    else:
        send_message(message, response_text=f'Ошибка.\n/help')

### MAIN ###            
if __name__ == '__main__':
    logging.critical('restart')
    bot.infinity_polling()
    