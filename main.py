import config
import telebot
import result
import teacher

bot = telebot.TeleBot(config.token)


class User:
    SAMPLE_SPREADSHEET_ID = ''
    SAMPLE_RANGE_NAME = ''
    counter = 0


# Делаем клавиатуру
def makeKeyboard_teacher():
    markup = telebot.types.InlineKeyboardMarkup()
    for key, value in teacher.teacher.items():
        markup.add(telebot.types.InlineKeyboardButton(text=key,
                                                      callback_data=value))
    return markup


def makeKeyboard_group_list():
    _groups = []
    _res = result.find_groups(User.SAMPLE_SPREADSHEET_ID)
    for i in range(len(_res)):
        title = _res[i].get("properties", {}).get("title", "Sheet1")
        _groups += [title]
    markup = telebot.types.InlineKeyboardMarkup()
    for i in _groups:
        markup.add(telebot.types.InlineKeyboardButton(text=i,
                                                      callback_data=i))
    return markup


# Приветствуем пользователя и говорим что умеем
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}, я помогу тебе узнать твои долги')
    bot.send_message(message.chat.id, 'Выбери преподавателя:', reply_markup=makeKeyboard_teacher())



@bot.callback_query_handler(func=lambda call: call.data in list(teacher.teacher.values()))
def handle_query(call):
    User.SAMPLE_SPREADSHEET_ID = call.data
    group_list(call.message)


def group_list(message):
    #bot.edit_message_reply_markup(message.chat.id, message.inline_message_id, 'g', reply_markup=makeKeyboard_group_list())
    bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id, reply_markup=None)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Выберите группу:', reply_markup=makeKeyboard_group_list())


@bot.callback_query_handler(func=lambda call: True)
def handle_query2(call):
    User.SAMPLE_RANGE_NAME = call.data
    bot.send_message(call.message.chat.id, 'Введите ваше ФИО')
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.register_next_step_handler(call.message, request_full_name)


def request_full_name(message):
    full_name = result.result_columns(User.SAMPLE_RANGE_NAME, User.SAMPLE_SPREADSHEET_ID)[0]
    for i in range(len(full_name)):
        if full_name[i].lower() == message.text.lower():
            User.counter = i
            break
    if User.counter == 0:
        bot.send_message(message.chat.id, 'Такого пользователя нет в базе')
        echo_text(message)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        btn1 = telebot.types.KeyboardButton('Узнать все оценки')
        btn2 = telebot.types.KeyboardButton('Что я сдал/сдала')
        btn3 = telebot.types.KeyboardButton('Что я должен/должна')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, f'Всего лабораторных работ: '
                f'{len(result.result_rows(User.SAMPLE_RANGE_NAME, User.SAMPLE_SPREADSHEET_ID)[User.counter]) - 2}',
                         reply_markup=markup)
        bot.register_next_step_handler(message, response_processing)


def response_processing(message):
    if message.text == 'Узнать все оценки':
        all_rating(message)
    elif message.text == 'Что я сдал/сдала':
        completed_works(message)
    elif message.text == 'Что я должен/должна':
        non_completed_works(message)
    else:
        echo_text(message)


def all_rating(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'вот тебе весь список', reply_markup=markup)
    rating = result.result_columns(User.SAMPLE_RANGE_NAME, User.SAMPLE_SPREADSHEET_ID)
    for i in range(len(rating)):
        bot.send_message(message.chat.id, f'{rating[i][0]} - {rating[i][User.counter]}')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn = telebot.types.KeyboardButton('/start')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Нажмите на кнопку, если хотите начать сначала', reply_markup=markup)




def completed_works(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'вот тебе весь список', reply_markup=markup)
    pass


def non_completed_works(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'вот тебе весь список', reply_markup=markup)
    pass


@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"])
def echo_text(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Попробуйте начать сначала', reply_markup=markup)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn = telebot.types.KeyboardButton('/start')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Нажмите на кнопку', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
