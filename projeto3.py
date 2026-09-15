import pickle
from collections import deque
from datetime import datetime
import faker

'''PARTE 1'''
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

'''PARTE 2'''
class Pagamento:

  def __init__(self, cliente_pagador, numero_comanda, forma_pagamento, valor_total):
    self.cliente_pagador = cliente_pagador
    self.numero_comanda = numero_comanda
    self.forma_pagamento = forma_pagamento  # "PIX", "cartao" ou "dinheiro"
    self.valor_total = valor_total
    self.data_hora_pagamento = datetime.now()

# Lista para armazenar o histórico de pagamentos realizados no restaurante
historico_pagamentos = []

def fechar_comanda(numero_comanda, forma_pagamento, tabela_precos):
    if numero_comanda not in comandas_abertas:
        print(f"ERRO: Comanda nº {numero_comanda} não encontrada ou já fechada!")
        return None

    comanda = comandas_abertas[numero_comanda]
    valor_total = 0.0

    #Soma os valores das refeições
    for item in comanda.refeicoes:
        valor_total+=tabela_precos.get(item,0.0)
    # Soma os valores das bebidas
    for item in comanda.bebidas:
        valor_total+=tabela_precos.get(item,0.0)

    novo_pagamento=Pagamento(cliente_pagador=comanda.cliente,
      numero_comanda=comanda.numero,
      forma_pagamento=forma_pagamento,
      valor_total=valor_total)


    historico_pagamentos.append(novo_pagamento)

    # Remove a comanda do dicionário de comandas abertas
    del comandas_abertas[numero_comanda]

    return novo_pagamento
