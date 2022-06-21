import pandas as pd
import logging

class Usuarios:
    @staticmethod    
    def get_users(self, _conta):
        try:
            contas_base = pd.read_excel('../datebase/contas.xlsx')
            for indice, conta in enumerate(contas_base['Contas']):
                if(conta == _conta):
                    fim = contas_base['Fim'][indice]
                    inicio = 1 if indice == 0 else contas_base['Fim'][indice-1]
            users_base = pd.read_excel('../datebase/usuarios.xlsx')
            users_with_1 = []
            for indice, user in enumerate(users_base['Enviados']):
                if user == 1 and (indice < fim and indice > inicio):
                    users_with_1.append(users_base['Usuários'][indice])
            logging.info('Base de usuários carregada com sucesso.')
            return users_with_1
        except Exception as e:
            logging.error('Não foi possível carregar base de usuários.')

