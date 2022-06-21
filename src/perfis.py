import pandas as pd
import logging 
from logging import FileHandler, StreamHandler
from datetime import date

logging.basicConfig(
    level = logging.INFO, 
    format= "%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d - %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[FileHandler("./logs/instabot-"+str(date.today())+".log", 'a'), StreamHandler()]
)

class Perfis:
    @staticmethod    
    def get_users(_conta):
        try:
            contas_base = pd.read_excel('./datebase/contas.xlsx')
            for indice, conta in enumerate(contas_base['Contas']):
                conta_encontrada= False
                if(conta == _conta):
                    fim = contas_base['Fim'][indice]-1
                    inicio = 0 if indice == 0 else contas_base['Fim'][indice-1]
                    conta_encontrada = True
                    print(inicio)
                    print(fim)
                    break
            if (conta_encontrada==False):
                logging.warning('Conta não econtrada na base de daods. Tente novamente.')
                exit()
            users_base = pd.read_excel('./datebase/perfis.xlsx')
            users_with_1 = []
            for indice, user in enumerate(users_base['Enviados']):
                if user == 1 and (indice <= fim and indice >= inicio):
                    users_with_1.append(users_base['Perfis'][indice])
            logging.info('Base de perfis carregada com sucesso.')
            print(users_with_1)
            return users_with_1
        except Exception as err:
            logging.error('Não foi possível carregar base de dados :: '+str(err))
            exit()
