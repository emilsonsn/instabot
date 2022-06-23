from asyncio import sleep
from os import EX_CANTCREAT
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
                time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(self.USERNAME)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(self.PASSWORD)
            self.browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(Keys.ENTER)
            esperar = 0 
            while len(self.browser.find_elements(By.CSS_SELECTOR, 'img[data-testid="user-avatar"]')) < 1:
                time.sleep(1)
                esperar+=1
                logging.warning('Autenticação demorando muito...') if esperar%15 == 0 else ''
                if esperar > 20:
                    logging.warning(f"Login está demorando muito. Usuário:' {self.USERNAME}")
                    self.browser.quit()
                    exit()
            logging.info('Login efetuado corretamente. Usuário:'+self.USERNAME)
            self.tirarNotificaocao()
        except Exception as err:
            logging.error(f"Erro inesperado ao tentar logar. Usuários:{str(err)} {self.USERNAME}")
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()

    def tirarNotificaocao(self):
        try:    
            self.browser.get('https://www.instagram.com/direct/inbox/')
            while(len(self.browser.find_elements(By.XPATH,"//button[text()='Agora não']")) < 1):
                time.sleep(1)
            self.browser.find_element(By.XPATH,"//button[text()='Agora não']").click()
            while(len(self.browser.find_elements(By.CSS_SELECTOR,'button')) < 1):
                time.sleep(1)
            self.browser.find_elements(By.CSS_SELECTOR,'button')[0].click()
            time.sleep(1)
            self.browser.find_elements(By.CSS_SELECTOR,'button')[0].send_keys(Keys.ESCAPE)    
        except Exception as err:
            logging.error(f"Erro ao tirar notificação. {str(err)} {self.USERNAME}")  
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()
            
    def find_profile(self):
        try:
            perfis = Perfis.get_perfis(self.USERNAME)
            if(len(perfis) > 0):
                for perfil in perfis:
                    self.INDICE_PERFIL = perfil[0]
                    self.NOME_PERFIL = perfil[1]
                    break
            else:
                logging.warning("Não existe perfis pendentes para a conta. Planilha necessita de atualização para a conta: "+self.USERNAME)
                self.sleep_for_time(10*60)
                self.main()
        except Exception as err:
            logging.error(f"Erro ao buscar perfis para a conta:{str(err)} {self.USERNAME}")
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()
            
    def random_message(self):
        try:
            return self.MESSAGES[random.randint(0,len(self.MESSAGES)-1)]
        except Exception as err:
            logging.error(f"Erro ao escolher mensagem aleatoriamente. {str(err)} {self.USERNAME}")
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()

    def sleep_for_time(self,minutos):
        try:
            logging.info("Entrando em espera... "+str(minutos/60)+" min")
            time.sleep(int(minutos))
        except Exception as err:
            logging.error(f"Erro ao entrar em modo de espera. {str(err)} {self.USERNAME}")
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()
            
    def send_message(self,message):
        try:
            self.browser.get('https://www.instagram.com/direct/inbox/')
            while(len(self.browser.find_elements(By.CSS_SELECTOR,'button')) < 1):
                time.sleep(1)
            self.browser.find_elements(By.CSS_SELECTOR,'button')[2].click()
            while(len(self.browser.find_elements(By.CSS_SELECTOR,'input')) < 1):
                time.sleep(1)
            self.browser.find_elements(By.CSS_SELECTOR,'input')[1].send_keys(self.NOME_PERFIL)        
            time.sleep(3)
            while(len(self.browser.find_elements(By.CSS_SELECTOR,'circle')) < 1):
                time.sleep(1)
            self.browser.find_elements(By.CSS_SELECTOR,'circle')[2].click()
            time.sleep(1)
            self.browser.find_element(By.XPATH,"//div[text()='Avançar']").click()
            while (len(self.browser.find_elements(By.CSS_SELECTOR, 'textarea'))<1):
                time.sleep(2)
            self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(message)
            time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(Keys.ENTER)
            logging.info("Mensagem enviada com sucesso!")
            Perfis.set_perfil(self.INDICE_PERFIL)
            Contas.set_count(self.USERNAME)
            time.sleep(1)
        except Exception as err:
            logging.error(f"Erro ao tentar enviar mensagem. {str(err)} {self.USERNAME}")
            logging.info(f"Reiniciando bot em 2 minuto.")
            self.restartBot()
                     
    def restartBot(self):
            self.browser.quit()
            self.sleep_for_time(2*60)
            logging.info("Reiniciando sistema automáticamente...")
            self.browser = webdriver.Chrome(service=service, options=Options.get_options())
            self.logar()
            self.main()        
            
    def main(self):
        try:
            self.find_profile()
            self.send_message(self.random_message())
            self.sleep_for_time(self.TEMPO_ESPERA)
            self.main()
        except Exception as err:
            self.restartBot()
            
bot = instabot()
bot.main()