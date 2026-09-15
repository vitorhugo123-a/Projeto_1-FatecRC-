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
#Dicionário do estoque do restaurante
estoque_restaurante={}

def adicionar_lote_estoque(
        nome,preco_compra,preco_venda,data_compra,data_vencimento,quantidade
):
    lote=produtoestoque(
        nome,preco_compra,preco_venda,data_compra,data_vencimento,quantidade
)
    if nome not in estoque_restaurante:
        estoque_restaurante[nome]=deque()
    estoque_restaurante[nome].append(lote)
    
def consumir_produto_velho(nome,quantidade_usada):
    #Retira do estoque priorizando os itens mais velhos
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
