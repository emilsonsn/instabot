from asyncio import sleep
import time
from numpy import rint
from src.config import Config
from selenium import webdriver
from gettext import find
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.config import Options
from src.perfis import Perfis
import random
from src.contas import Contas
from src.log_config import LogConfig
from src.telegrambot import BotTelegram
from selenium.webdriver.chrome.service import Service

logging = LogConfig.get_logging()
service = Service('./chromedriver')

class instabot:
    def __init__(self):       
        self.MESSAGES = [
            Config.get_conf()['msg1'],
            Config.get_conf()['msg2'],
            Config.get_conf()['msg3']
            ]
        self.TEMPO_ESPERA = Config.get_conf()['tempo_espera']
        self.USERNAME = input('Digite o username da conta: ')
        self.PASSWORD = input('Digite a senha da conta: ')
        self.browser = webdriver.Chrome(service=service, options=Options.get_options())
        self.INDICE_PERFIL = 0
        self.logar()
    def logar(self):
        try:
            self.browser.get('https://instagram.com')
            while len(self.browser.find_elements(By.CSS_SELECTOR, 'input[name="username"]')) < 1:
                time.sleep(0.5)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(self.USERNAME)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(self.PASSWORD)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(Keys.ENTER)
            esperar = 0 
            while len(self.browser.find_elements(By.CSS_SELECTOR, 'img[data-testid="user-avatar"]')) < 1:
                time.sleep(1)
                esperar+=1
                logging.warning('Autenticação demorando muito...') if esperar%15 == 0 else ''
                if esperar > 20:
                    logging.warning('Não foi possível efetuar o login corretamente. Usuário:'+self.USERNAME)
                    self.browser.quit()
                    exit()
            logging.info('Login efetuado corretamente. Usuário:'+self.USERNAME)
        except Exception as err:
            logging.error('Erro inesperado ao tentar logar. Usuários:'+self.USERNAME+str(err))
            self.browser.quit()
            exit()

    def find_profile(self):
        perfis = Perfis.get_perfis(self.USERNAME)
        if(len(perfis) > 0):
            for perfil in perfis:
                self.INDICE_PERFIL = perfil[0]
                self.browser.get('https://instagram.com/'+perfil[1])
                break
        else:
            logging.warning("Não existe perfis pendentes para a conta. Planilha necessita de atualização para a conta: "+self.USERNAME)
            self.sleep_for_time(10*60)
            self.main()

    def random_message(self):
        return self.MESSAGES[random.randint(0,len(self.MESSAGES)-1)]

    def sleep_for_time(self,minutos):
        logging.info("Entrando em espera... "+str(minutos/60)+" min")
        time.sleep(int(minutos))

    def send_message(self,message):
        time.sleep(5)
        esperar = 0
        while(len(self.browser.find_elements(By.XPATH, "//*[text()='Enviar mensagem']")) < 1):
            time.sleep(1)
            esperar+=1
            if esperar == 25:
                Perfis.set_perfil_error(self.INDICE_PERFIL)
                self.main()

        self.browser.find_element(By.XPATH,"//*[text()='Enviar mensagem']").click()
        while (len(self.browser.find_elements(By.CSS_SELECTOR, 'textarea'))<1):
            time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(message)
        self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(Keys.ENTER)
        logging.info("Mensagem enviada com sucesso!")
        Perfis.set_perfil(self.INDICE_PERFIL)
        Contas.set_count(self.USERNAME)
        time.sleep(1)

    def main(self):
        try:
            self.find_profile()
            self.send_message(self.random_message())
            self.sleep_for_time(self.TEMPO_ESPERA)
            self.main()
        except Exception as err:
            logging.critical('Problema inesperado na execução do script. '+str(err))
            logging.info("Reiniciando sistema em 5 minutos...")
            BotTelegram.send_message("Mensagem de erro interna do sistema: "+str(err))
            self.sleep_for_time(5*60)
            self.browser.refresh()
            self.main()
bot = instabot()
bot.main()