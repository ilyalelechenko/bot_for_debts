import config
import telebot
import teacher
from googleapiclient.discovery import build


bot = telebot.TeleBot(config.token)
service = build('sheets', 'v4', credentials=config.credentials)
sheet = service.spreadsheets()
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = ''


# Делаем клавиатуру
def makeKeyboard_teacher():
    markup = telebot.types.InlineKeyboardMarkup()
    for key, value in teacher.teacher.items():
        markup.add(telebot.types.InlineKeyboardButton(text=key,
                                                      callback_data=value))
    return markup


def makeKeyboard_group_list():
    groups = []
    result = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    res = result.get('sheets', '')
    for i in range(len(res)):
        title = res[i].get("properties", {}).get("title", "Sheet1")
        groups += [title]
    markup = telebot.types.InlineKeyboardMarkup()
    for i in groups:
        markup.add(telebot.types.InlineKeyboardButton(text=i,
                                                      callback_data=i))
    return markup


# Приветствуем пользователя и говорим что умеем
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! я помогу тебе узнать твои долги')
    bot.send_message(message.chat.id, 'Выбери своего преподавателя', reply_markup=makeKeyboard_teacher())


@bot.callback_query_handler(func=lambda call: call.data in list(teacher.teacher.values()))
def handle_query(call):
    global SAMPLE_SPREADSHEET_ID
    SAMPLE_SPREADSHEET_ID = call.data
    group_list(call.message)


def group_list(message):
    bot.send_message(message.chat.id, 'Выберите группу', reply_markup=makeKeyboard_group_list())


@bot.callback_query_handler(func=lambda call: True)
def handle_query2(call):
    global SAMPLE_RANGE_NAME
    SAMPLE_RANGE_NAME = call.data
    test(call.message)


def test(message):
    bot.send_message(message.chat.id, 'Введите ваше фио')


# Call the Sheets API
"""
result_columns = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME, majorDimension='COLUMNS').execute()
result_rows = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                 range=SAMPLE_RANGE_NAME, majorDimension='ROWS').execute()
values_columns = result_columns.get('values', [])
values_rows = result_columns.get('values', [])

fio = values[0]
print(fio)
for i in range(len(fio)):
    if fio[i] == 'Лелеченко':
        counter = i
        break
print(counter)
print(f' Всего у вас {len(values) - 2}, лабораторных работ')
print(*values2[counter])
"""
if __name__ == '__main__':
    bot.polling(none_stop=True)
