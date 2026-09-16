def popular_faker(qtd_comandas=3, qtd_produtos=3):
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
      comandas=comandas(num,nome_cliente)

      comandas.adicionar_refeicao('Prato Feito')
      comandas.adicionar_refeicao(
         random.choice(['Coca-Cola','Suco','Água'])
      )
      comandas_abertas[num]=comandas


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