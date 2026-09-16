import pickle
from collections import deque
from datetime import datetime
import random
from faker import Faker

fake = Faker('pt_BR')

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


class produtoestoque:

    def __init__(self,nome,preco_compra,preco_venda,data_compra,data_vencimento,quantidade):
        self.nome=nome
        self.preco_compra=preco_compra
        self.preco_venda=preco_venda
        self.data_compra=data_compra
        self.data_vencimento=data_vencimento
        self.quantidade=quantidade

    def editar_quantidade(self,nova_quantidade):
        self.quantidade=nova_quantidade

estoque_restaurante={}

def adicionar_lote_estoque(nome,preco_compra,preco_venda,data_compra,data_vencimento,quantidade):
    lote=produtoestoque(nome,preco_compra,preco_venda,data_compra,data_vencimento,quantidade)
    if nome not in estoque_restaurante:
        estoque_restaurante[nome]=deque()
    estoque_restaurante[nome].append(lote)

def consumir_produto_velho(nome,quantidade_usada):
    #Retira do estoque priorizando os itens mais velhos(fila)
    if nome not in estoque_restaurante or len(estoque_restaurante[nome])==0:
        print(f"Produto {nome} não possui estoque disponível")
        return False

    lote_mais_antigo=estoque_restaurante[nome][0]
    if lote_mais_antigo.quantidade>=quantidade_usada:
        lote_mais_antigo.quantidade-=quantidade_usada
        #se a quantidade do lote zerar, remove o lote da fila
        if lote_mais_antigo.quantidade==0:
            estoque_restaurante[nome].popleft()
        return True
    else:
        print(f"Quantidade insuficiente no lote mais antigo de {nome}")
        return False


class Pagamento:

  def __init__(
      self,
      cliente_pagador,
      numero_comanda,
      forma_pagamento,
      valor_total,
      itens_consumidos,
  ):
    self.cliente_pagador = cliente_pagador
    self.numero_comanda = numero_comanda
    self.forma_pagamento = forma_pagamento
    self.valor_total = valor_total
    self.itens_consumidos = itens_consumidos
    self.data_hora_pagamento = datetime.now()
# Lista para armazenar o histórico de pagamentos realizados no restaurante
historico_pagamentos = []

def fechar_comanda(numero_comanda, forma_pagamento, tabela_precos):
    if numero_comanda not in comandas_abertas:
        print(f"ERRO: Comanda nº {numero_comanda} não encontrada ou já fechada!")
        return None

    comanda = comandas_abertas[numero_comanda]
    valor_total = 0.0
    for item in comanda.refeicoes:
        valor_total+=tabela_precos.get(item,0.0)
    for item in comanda.bebidas:
        valor_total+=tabela_precos.get(item,0.0)

    novo_pagamento=Pagamento(cliente_pagador=comanda.cliente,
      numero_comanda=comanda.numero,
      forma_pagamento=forma_pagamento,
      valor_total=valor_total)
    historico_pagamentos.append(novo_pagamento)

    del comandas_abertas[numero_comanda]
    return novo_pagamento

ingredientes_refeicoes = {
    "Prato Feito - Bife": [("Arroz", 1), ("Bife", 1)],
    "Coca-Cola": [("Coca-Cola", 1)],
    "Suco": [("Suco", 1)],
    "Água": [("Água", 1)],
}

def fechar_comanda_com_baixa(numero_comanda, forma_pagamento, tabela_precos_venda):
  if numero_comanda not in comandas_abertas:
    return None
  comanda = comandas_abertas[numero_comanda]
  valor_total = 0.0
  todos_os_itens = comanda.refeicoes + comanda.bebidas

# Dá baixa no estoque de cada ingrediente/bebida (FIFO)
  for item in todos_os_itens:
    if item in ingredientes_refeicoes:
      for ingrediente, qtd in ingredientes_refeicoes[item]:
        consumir_produto_velho(ingrediente, qtd)

    valor_total += tabela_precos_venda.get(item, 0.0)

    # Registra o pagamento e o consumo do cliente
  registro_pagamento = Pagamento(
      cliente_pagador=comanda.cliente,
      numero_comanda=comanda.numero,
      forma_pagamento=forma_pagamento,
      valor_total=valor_total,
      itens_consumidos=list(todos_os_itens),
  )
  historico_pagamentos.append(registro_pagamento)

  del comandas_abertas[numero_comanda]
  return registro_pagamento


def popular_faker(qtd_comandas=3, qtd_produtos=5):
    for _ in range(qtd_produtos):
      #escolhe uma palavra e deixa a 1º letra maiuscula
      nome_prod=fake.word().capitalize()
      if nome_prod not in estoque_restaurante:
         estoque_restaurante[nome_prod]=deque()

      lote=produtoestoque(
         nome=nome_prod,
        preco_compra=round(random.uniform(2.0, 10.0), 2),#gera um número aleatório até 2 casas decimais
        preco_venda=round(random.uniform(11.0, 30.0), 2),
        data_compra=fake.date_this_year().strftime("%Y-%m-%d"),#gera data da compra
        data_vencimento=fake.future_date().strftime("%Y-%m-%d"),#gera data do vencimento
        quantidade=random.randint(10, 50),
      )
      estoque_restaurante[nome_prod].append(lote)

    #popula com cliente
    for _ in range(qtd_comandas):
      num=random.randint(100,999)
      nome_cliente=fake.name()
      nova_comanda=comanda(num,nome_cliente)

      nova_comanda.adicionar_refeicao('Prato Feito')
      nova_comanda.adicionar_bebida(
         random.choice(['Coca-Cola','Suco','Água'])
      )
      comandas_abertas[num]=nova_comanda


def salvar_dados_sistema(nome_arquivo='dados_restaurante.pkl'):#salva as estruturas em arquivo binário
    dados={
       'comandas':comandas_abertas,
       'estoque':estoque_restaurante,
       'pagamentos':historico_pagamentos,
    }
    with open(nome_arquivo,'wb')as arquivo:
       pickle.dump(dados,arquivo)

def carregar_dados_sistema(nome_arquivo='dados_restaurante.pkl'):#carrega as estruturas salvas
    global comandas_abertas,estoque_restaurante,historico_pagamentos
    try:
        with open(nome_arquivo,'rb')as arquivo:
            dados=pickle.load(arquivo)
            comandas_abertas=dados['comandas']
            estoque_restaurante=dados['estoque']
            historico_pagamentos=dados['pagamentos']
    except FileNotFoundError:
       pass


def relatorio_vendas():
    total_faturado=0.0
    print('\n--- RELATÓRIO DE VENDAS ---')
    print(f'Total de comandas pagas: {len(historico_pagamentos)}')

    for p in historico_pagamentos:
      total_faturado += p.valor_total
      print(
         f'Comanda {p.numero_comanda} | Cliente: {p.cliente_pagador} | Valor: R$'
         f' {p.valor_total:.2f} | Forma: {p.forma_pagamento}'
      )

    print(f'Faturamento Total: R$ {total_faturado:.2f}')

def relatorio_consumo():
    contagem_itens= {}
    for p in historico_pagamentos:
       for item in p.itens_consumidos:
          contagem_itens[item]=contagem_itens.get(item, 0) + 1

    print('\n--- Relatório de Consumo ---')
    for item, qtd in contagem_itens.items():
       print(f'Item: {item} | Total consumido: {qtd} unidades')


   
      
    





# ==========================================
# BLOCO DE TESTE / EXECUÇÃO
# ==========================================
if __name__ == "__main__":
  print("=== POPULANDO O SISTEMA ===")
  popular_faker(qtd_comandas=3, qtd_produtos=5)

  # Tabela de preços simples para o teste
  tabela_precos = {
      "Prato Feito": 25.00,
      "Coca-Cola": 6.00,
      "Suco": 8.00,
      "Água": 4.00,
  }

  # Pegamos a primeira comanda aberta criada pelo Faker para fechar
  if comandas_abertas:
    primeiro_num = list(comandas_abertas.keys())[0]
    print(f"\nFechando comanda nº {primeiro_num}...")
    fechar_comanda_com_baixa(
        primeiro_num, "PIX", tabela_precos_venda=tabela_precos
    )

  # Chamando os relatórios para exibir no terminal
  relatorio_vendas()
  relatorio_consumo()

  # Testando o salvamento e carregamento
  salvar_dados_sistema()
  print("\nDados salvos!")
