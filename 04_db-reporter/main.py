import utils
logger = utils.get_logger(__name__)
from database import DataBase
import yaml
with open("config.yml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
    token = cfg["telegram"]['token']  
    cache = cfg['path']['cache']
    db_params = cfg['database']
tg = utils.Telegram(token)
db = DataBase(db_params)

### FUNCTIONS ###
def main_func(message):
    cond = 'NULL' if str(message.text) == '' else str(message.text)
    df = db.request('request.sql', conditions=cond)
    if not os.path.exists(cache):
        os.makedirs(cache)
    file_name = os.path.join(cache, f'table_{condition}.xlsx')
    if os.path.exists(file_name):
        os.remove(file_name)
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "title"
    wb.save(file_name)
    with pd.ExcelWriter(file_name, datetime_format='DD/MM/YYYY') as writer:
        df.to_excel(writer, sheet_name='sheet', index=False)
    return file_name

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
        with open(result, 'rb') as f: 
            tg.send_document(message, f)
    else:
        tg.send_message(message, response_text=f'Ошибка.\n/help')

### MAIN ###            
if __name__ == '__main__':
    tg.infinity_polling()