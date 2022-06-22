from click import command
import telebot

class BotTelegram:
    @staticmethod
    def send_message(mensagem):
        CHAVE_API = "5532192507:AAEkAhCiEPeofGjK03ApJ61LEXrp4TIhOog"
        bot = telebot.TeleBot(CHAVE_API)
        bot.send_message(1990212496,"Ops.. Houve algum problema em uma das intâncias do seu bot do instagram.")
        bot.send_message(1990212496,mensagem)
