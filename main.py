import telebot
from telebot import types
import requests
import gtts
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from io import BytesIO


state_storage = StateMemoryStorage()
bot = telebot.TeleBot('6410028806:AAEj6qvptWTFBw7hq4R56jm4vy6voJ2ohm4', state_storage=state_storage)


def random_image(call):
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format('')
    response = requests.get(api_url, headers={'X-Api-Key': 'hlQrVwQodLAclysWGSigeA==5hMEsWtU3AI9I5Qt', 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        bot.send_photo(call.from_user.id, response.raw)
    else:
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, "Ошибка")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Привет, боту можно написать:\n"
                                           "1) Audio - работа с аудиофайлами\n"
                                           "2) Photo - работа с картинками\n"
                                           "3) Repos - ссылка на репозиторий")
    bot.set_state(message.from_user.id, 1, message.chat.id)


@bot.message_handler(state=1, content_types=['text'])
def receive_message(message):
    if message.text == 'Audio':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_rickroll = types.InlineKeyboardButton(text="rickroll", callback_data="rickroll")
        keyboard.add(key_rickroll)
        key_texttosound = types.InlineKeyboardButton(text="texttosound", callback_data="gtts")
        keyboard.add(key_texttosound)
        bot.send_message(message.from_user.id, "Выбери аудиофайл", reply_markup=keyboard)
    if message.text == 'Image':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_random = types.InlineKeyboardButton(text="random", callback_data="rng")
        keyboard.add(key_random)
        key_car = types.InlineKeyboardButton(text="car", callback_data="Car")
        keyboard.add(key_car)
        bot.send_message(message.from_user.id, "Выбери картинку", reply_markup=keyboard)


@bot.message_handler(content_types=['text'], state=2)
def message_to_voice(message):
    bot.set_state(message.from_user.id, 1)
    sound = BytesIO()
    tts = gtts.gTTS(str(message.text), lang='en')
    tts.write_to_fp(sound)
    sound.seek(0)
    bot.send_audio(message.from_user.id, sound)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "rickroll":
        f = open(r'rickroll.MP3', 'rb')
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_audio(call.from_user.id, f)
        f.close()
    elif call.data == "rng":
        bot.delete_message(call.from_user.id, call.message.message_id)
        random_image(call)
    elif call.data == "Car":
        f = open(r'test.jpg', 'rb')
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_photo(call.from_user.id, f)
        f.close()
    elif call.data == "gtts":
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.set_state(call.from_user.id, 2)
        bot.send_message(call.from_user.id, "Введи текст")


bot.add_custom_filter(custom_filters.StateFilter(bot))


bot.polling(none_stop=True, interval=0)
