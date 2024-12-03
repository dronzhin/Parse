import telebot
from cachetools import cached, TTLCache
from parse import parser
import time

# Настройка кеша
cache = TTLCache(maxsize=10, ttl=300)  # Кеш с временем жизни 5 минут

# Кешируемая функция парсинга
@cached(cache)
def parser_cash():
    time.sleep(5)
    result = parser()
    return result

# Чтение токена из файла
path_token = 'token.txt'
with open(path_token) as f:
    TOKEN = f.read().strip()

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Прикурить есть?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Сам только первый день работаю")

# Обработчик команды /parser
@bot.message_handler(commands=['parser'])
def send_parser(message):
    bot.reply_to(message, "Запускаю парсер...")
    result = parser_cash()  # Вызов кешируемой функции
    bot.reply_to(message, result)  # Отправка результата пользователю

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, f"{message.text} - очень интересно")

if __name__ == '__main__':
    bot.polling()
