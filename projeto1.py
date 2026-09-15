import pickle
from collections import deque
from datetime import datetime
import faker

class comanda:

    def __init__(self,numero,cliente):
        #atributos
        self.numero=numero
        self.cliente=cliente
        # registra a data e hora da abertura
        self.data_hora_abertura=datetime.now()
        #lista pra armazenar itens
        self.refeicoes=[]
        self.bebidas=[]

    def adicionar_refeicao(self,refeicao):
        self.refeicoes.append(refeicao)

    def remover_refeicao(self,refeicao):
        if refeicao in self.refeicoes:
            self.refeicoes.remove(refeicao)
            return True
        return False

    def adicionar_bebida(self,bebida):
        self.bebidas.append(bebida)

    def remover_bebida(self,bebida):
        if bebida in self.bebidas:
            return True
        return False

comandas_abertas={}
