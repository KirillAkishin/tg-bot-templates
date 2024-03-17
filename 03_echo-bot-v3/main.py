import utils
logger = utils.get_logger(__name__)
import yaml
with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  
tg = utils.Telegram(token)

### FUNCTIONS ###
def main_func(message):
    text = str(message.text)
    return text if text != '' else None

### HANDLERS ###
@tg.message_handler(commands=["help"])
def help_processing(message):
    logger.warning('/help')
    tg.send_message(message, response_text='Помощь.')
    
@tg.message_handler(content_types=["text"])
def text_processing(message): 
    logger.warning(message.text)
    tg.send_message(message, response_text='Обработка запроса.')
    result = main_func(message)
    if result:
        tg.send_message(message, response_text=result)
    else:
        tg.send_message(message, response_text=f'Ошибка.\n/help')

### MAIN ###            
if __name__ == '__main__':
    tg.infinity_polling()