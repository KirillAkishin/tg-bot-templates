import os
import pandas as pd
import utils
logger = utils.get_logger(__name__)
from database import DataBase
import yaml
with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  
    data_dir = cfg['path']['data']
    db_params = cfg['database']
tg = utils.Telegram(token)
db = DataBase(db_params)

### FUNCTIONS ###
def get_excel_from_db(message):
    cond = 'NULL' if str(message.text) == '' else str(message.text)
    df = db.conn.request('database/request.sql', conditions=cond)
    filename = os.path.join(data_dir, f'table_{cond}.xlsx')
    utils.save_excel(df, filename)
    return open(filename, 'rb')

def get_excel_from_file(message):
    table_name = 'NULL' if str(message.text) == '' else str(message.text)
    filename = os.path.join(data_dir, f'{table_name}.xlsx')
    return open(filename, 'rb')

### HANDLERS ###
@tg.message_handler(commands=["help"])
def help_processing(message):
    logger.warning('/help')
    tg.send_message(message, response_text='Помощь.')
    
@tg.message_handler(content_types=["text"])
def text_processing(message): 
    logger.warning(message.text)
    tg.send_message(message, response_text='Обработка запроса.')
    result = get_excel_from_db(message)
#     result = get_excel_from_file(message)
    if result:
        tg.send_document(message, result)
    else:
        tg.send_message(message, response_text=f'Ошибка.\n/help')

### MAIN ###            
if __name__ == '__main__':
    tg.infinity_polling()