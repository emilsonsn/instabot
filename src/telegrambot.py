from click import command
import telebot

class BotTelegram:
    @staticmethod
    def send_message(mensagem, telegramConfig):
        telegram = telegramConfig
        bot = telebot.TeleBot(telegram['chave_api_telegram'])
        bot.send_message(telegram['my_id_telegram'], "Ops.. Houve algum problema em uma das intâncias do seu bot do instagram.")
        bot.send_message(telegram['my_id_telegram'], mensagem)

