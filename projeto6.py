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