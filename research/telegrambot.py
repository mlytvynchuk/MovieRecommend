import telebot
import film_recommender
from telebot import types


bot = telebot.TeleBot("898784203:AAEvbzX5R1nHG8gCcI7Dlp5O1zP4ZHCddys")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello, I am your personal Movie Recommender\n Write /help to get info")


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Just write your movie name that you have already watched to find similar ones")


@bot.message_handler(content_types=['text'])
def send_data(message):
    i = 0
    films = ""
    films = film_recommender.find_simulars(message.text)
    if len(films)>0:
        data = "We recommend you to watch:\n" + "\n".join(films)
        bot.send_message(message.chat.id, data)
    else:
         bot.send_message(message.chat.id, "Please try again with another title")

if __name__ == "__main__":
    bot.polling()
    