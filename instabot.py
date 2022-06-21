from asyncio import sleep
import logging
import time
from numpy import rint
from src.config import Config
from selenium import webdriver
from gettext import find
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.config import Options
from logging import FileHandler, StreamHandler
from datetime import date
from src.perfis import Perfis
import random
logging.basicConfig(
    level = logging.INFO, 
    format= "%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d - %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[FileHandler("./logs/instabot-"+str(date.today())+".log", 'a'), StreamHandler()]
)



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
        self.browser = webdriver.Chrome('chromedriver', options=Options.get_options())
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
                    exit()
            logging.info('Login efetuado corretamente. Usuário:'+self.USERNAME)
        except Exception as err:
            logging.error('Erro inesperado ao tentar logar. Usuários:'+self.USERNAME+str(err))
            self.browser.close()
            exit()

    def find_profile(self):
        perfis = Perfis.get_perfis(self.USERNAME)
        if(len(perfis) > 0):
            for perfil in perfis:
                self.INDICE_PERFIL = perfil[0]
                self.browser.get('https://instagram.com/'+perfil[1])
                break
        else:
            logging.warning("Não existe perfis pendentes para esse perfil."+perfil[1])


    def random_message(self):
        return self.MESSAGES[random.randint(0,2)]

    def sleep_for_time(self):
        logging.info("Entrando em espera... "+str(self.TEMPO_ESPERA/1000)+" minutos")
        time.sleep(int(self.TEMPO_ESPERA))

    def send_message(self,message):
        time.sleep(5)
        while(len(self.browser.find_elements(By.XPATH, "//*[text()='Enviar mensagem']")) < 1):
            time.sleep(2)
        self.browser.find_element(By.XPATH,"//*[text()='Enviar mensagem']").click()
        while (len(self.browser.find_elements(By.CSS_SELECTOR, 'textarea'))<1):
            time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(message)
        self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(Keys.ENTER)
        Perfis.set_perfil(self.INDICE_PERFIL)
        time.sleep(1)

    def main(self):
        try:
            self.find_profile()
            self.send_message(self.random_message())
            self.sleep_for_time()
            self.main()
        except Exception as err:
            logging.critical('Problema inesperado na execução do script.'+str(err))
            logging.info("Reiniciando sistema...")
            self.browser.quit()
            self.browser = webdriver.Chrome('chromedriver', options=Options.get_options())
            self.main()

bot = instabot()
bot.main()