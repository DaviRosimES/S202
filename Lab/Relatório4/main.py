from database import Database
from productanalyzer import ProductAnalyzer

def main():
    db = Database(database="mercado", collection="compras")
    #db.resetDatabase()

    analyzer = ProductAnalyzer(db)

    analyzer.totalVendasDia()
    analyzer.clienteQueMaisGastouEmUmaCompra()
    analyzer.produtoMaisVendidoEmTodasAsCompras()
    analyzer.produtoVendidoAcimaDeUmaUnidade()


if __name__ == "__main__":
    main()
