import math
from math import nan
from numpy import NaN
import pandas as pd
from src.log_config import LogConfig

logging = LogConfig.get_logging()
class Contas:
    @staticmethod  
    def set_count(username):
        try:
            contas_base = pd.read_excel('./datebase/contas.xlsx')
            new_value = 1 if math.isnan(contas_base["Enviados"][contas_base["Contas"]==username]) else int(contas_base["Enviados"][contas_base["Contas"]==username])+1
            contas_base.loc[contas_base["Contas"]==username, "Enviados"] = new_value
            contas_base.to_excel("./datebase/contas.xlsx",index=False)
            logging.info('Contador atualizado.')
        except Exception as e:
            logging.warning('Não foi possível atualizar planilha de contas.')
            