import logging
import time
from src.config import Config
from selenium import webdriver
from gettext import find
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.config import Options
from logging import FileHandler, StreamHandler
from datetime import date
from src.usuarios import Usuarios

logging.basicConfig(
    level = logging.INFO, 
    format= "%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d - %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[FileHandler("./logs/instabot-"+str(date.today())+".log", 'a'), StreamHandler()]
)
MENSAGENS = [
    Config.get_conf()['msg1'],
    Config.get_conf()['msg2'],
    Config.get_conf()['msg3']
    ]
TEMPO_ESPERA = Config.get_conf()['tempo_espera']
USERNAME = input('Digite o username da conta: ')
PASSWORD = input('Digite a senha da conta: ')

def logar():
    try:
        browser = webdriver.Chrome('chromedriver', options=Options.get_options())
        browser.get('https://instagram.com')
        while len(browser.find_elements(By.CSS_SELECTOR, 'input[name="username"]')) < 1:
            time.sleep(0.5)
        browser.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(USERNAME)
        browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(PASSWORD)
        browser.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(Keys.ENTER)
        esperar = 0 
        while len(browser.find_elements(By.CSS_SELECTOR, 'img[data-testid="user-avatar"]')) < 1:
            time.sleep(1)
            esperar+=1
            print('Autenticação demorando muito...') if esperar%15 == 0 else ''
            if esperar > 20:
                logging.warning('Não foi possível efetuar o login corretamente. Usuário:'+USERNAME)
                exit()
        logging.info('Login efetuado corretamente. Usuário:'+USERNAME)
    except:
        logging.error('Erro inesperado ao tentar logar. Usuários:'+USERNAME)

def find_profile():
    usuarios = Usuarios.get_users('sfdf')
logar()
