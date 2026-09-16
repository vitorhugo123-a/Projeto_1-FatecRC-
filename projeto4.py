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

# Dá baixa no estoque de cada produto (FIFO)
  for item in todos_os_itens:
    if item in ingredientes_refeicoes:
      for ingrediente, qtd in ingredientes_refeicoes[item]:
        consumir_produto_velho(ingrediente, qtd)

    valor_total += tabela_precos_venda.get(item, 0.0)

    # Registra o pagamento e consumo do cliente
  registro_pagamento = Pagamento(
      cliente_pagador=comanda.cliente,
      numero_comanda=comanda.numero,
      forma_pagamento=forma_pagamento,
      valor_total=valor_total,
      itens_consumidos=list(todos_os_itens),
  )
  # Remove a comanda das comandas abertas
  historico_pagamentos.append(registro_pagamento)

  del comandas_abertas[numero_comanda]
  return registro_pagamento
    