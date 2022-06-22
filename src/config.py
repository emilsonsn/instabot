import json
from pyexpat.errors import XML_ERROR_FINISHED
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Config:
    @staticmethod
    def get_conf():
        with open('config.json', 'r') as config:
            config = json.load(config)
            TEMPO_ESPERA_MIN = config['tempo_de_espera']*60
            MENSAGEM1 = config['mensagens']['mensagem1']
            MENSAGEM2 = config['mensagens']['mensagem2']
            MENSAGEM3 = config['mensagens']['mensagem3']
        return {
            "tempo_espera":TEMPO_ESPERA_MIN,
            "msg1": MENSAGEM1,
            "msg2": MENSAGEM2,
            "msg3": MENSAGEM3
        }
        
class Options:
    @staticmethod
    def get_options():
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=700,800")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("disable-infobars")
        return options
    
class Telegram:
    @staticmethod
    def get_telegram():
        with open('config.json', 'r') as config:
            config = json.load(config)
            id = config['my_id_telegram']
            return {
                "chave_api_telegram": config['chave_api_telegram'],
                "my_id_telegram": config['my_id_telegram']
            }

 