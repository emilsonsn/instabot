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
    def get_perfis(_conta):
        try:
            contas_base = pd.read_excel('./datebase/contas.xlsx')
            for indice, conta in enumerate(contas_base['Contas']):
                conta_encontrada= False
                if(conta == _conta):
                    fim = contas_base['Fim'][indice]-1
                    inicio = 0 if indice == 0 else contas_base['Fim'][indice-1]
                    conta_encontrada = True
                    break
            if (conta_encontrada==False):
                logging.warning('Conta não econtrada na base de daods. Tente novamente.')
                exit()
            perfis_base = pd.read_excel('./datebase/perfis.xlsx')
            perfis_with_1 = []
            for indice, user in enumerate(perfis_base['Enviados']):
                if user == 1 and (indice <= fim and indice >= inicio):
                    perfis_with_1.append([indice,perfis_base['Perfis'][indice]])
            logging.info('Base de perfis carregada com sucesso.')
            return perfis_with_1
        except Exception as err:
            logging.error('Não foi possível carregar base de dados :: '+str(err))
            exit()

    @staticmethod    
    def set_perfil(indice):
            try:
                perfis_base = pd.read_excel('./datebase/perfis.xlsx')
                perfis_base.loc[indice, "Enviados"] = 1
                perfis_base.to_excel("./datebase/perfis.xlsx",index=False)
                logging.info('Perfil atualizado. :'+perfis_base['Perfis'][indice]+':')
            except Exception as err:
                logging.error('Erro ao atualizar perfil na base de dados. :'+perfis_base['Perfis'][indice]+':'+str(err))


