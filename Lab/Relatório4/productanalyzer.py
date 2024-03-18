from database import Database
from utils.writeAJson import writeAJson

class ProductAnalyzer:
    def __init__(self, database : Database):
        self.db = database


    def totalVendasDia(self):
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id" : "$data_compra" , "total" : {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"_id": 1}}
        ])
        writeAJson(result, "Total_de_vendas_por_dia")


    def produtoMaisVendidoEmTodasAsCompras(self):
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Produto_mais_vendido_em_todas_as_compras")


    def clienteQueMaisGastouEmUmaCompra(self):
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group" : {"_id" : "$cliente_id" , "total" : {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort" : {"total" : -1}},
            {"$limit" : 1}
        ])
        writeAJson(result, "Cliente_que_mais_gastou_em_uma_compra")


    def produtoVendidoAcimaDeUmaUnidade(self):
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}},
            {"$match": {"total": {"$gt": 1}}}
        ])
        writeAJson(result, "Produto_vendido_acima_de_uma_unidade")