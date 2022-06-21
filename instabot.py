from asyncio import sleep
import logging
import time

from numpy import rint
from src.config import Config
import selenium
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
MESSAGES = [
    Config.get_conf()['msg1'],
    Config.get_conf()['msg2'],
    Config.get_conf()['msg3']
    ]
TEMPO_ESPERA = Config.get_conf()['tempo_espera']
USERNAME = input('Digite o username da conta: ')
PASSWORD = input('Digite a senha da conta: ')
browser = webdriver.Chrome('chromedriver', options=Options.get_options())

def logar():
    try:
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
    except Exception as err:
        logging.error('Erro inesperado ao tentar logar. Usuários:'+USERNAME+str(err))
        browser.close()
        exit()

def find_profile():
    perfis = Perfis.get_users(USERNAME)
    if(len(perfis) > 0):
        for perfil in perfis:
            browser.get('https://instagram.com/'+perfil)
            break

def random_message():
    return MESSAGES[random.randint(0,2)]

def sleep_for_time():
    time.sleep(int(TEMPO_ESPERA))

def send_message(message):
    time.sleep(5)
    while(len(browser.find_elements(By.XPATH, "//*[text()='Enviar mensagem']")) < 1):
        time.sleep(2)
    browser.find_element(By.XPATH,"//*[text()='Enviar mensagem']").click()
    while (len(browser.find_elements(By.CSS_SELECTOR, 'textarea'))<1):
        time.sleep(2)
    print('achou')
    browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(message)
    browser.find_element(By.CSS_SELECTOR, 'textarea').send_keys(Keys.ENTER)
    print('terminou')
    time.sleep(1)

def main():
    logar()
    find_profile()
    send_message(random_message())
    sleep_for_time()
    #main()

main()