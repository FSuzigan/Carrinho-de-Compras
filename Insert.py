import mysql.connector

class CarrinhodeCompras:
    def __init__(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="carrinho de compras"
            )
            self.cursor = self.conexao.cursor()
            print("✅ Conectado ao banco de dados com sucesso.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao conectar com o banco de dados: {err}")

    def adicionar_categoria(self, nome_categoria):
        try:
            query = "INSERT INTO categorias (nome_categoria) VALUES (%s)"
            self.cursor.execute(query, (nome_categoria,))
            self.conexao.commit()
            print("✅ Categoria adicionada com sucesso.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao adicionar categoria: {err}")

    def listar_categorias(self):
        try:
            query = "SELECT id_categoria, nome_categoria FROM categorias"
            self.cursor.execute(query)
            categorias = self.cursor.fetchall()
            if categorias:
                print("\n📦 Categorias disponíveis:")
                for cat in categorias:
                    print(f"ID: {cat[0]} - Nome: {cat[1]}")
            else:
                print("⚠️ Nenhuma categoria encontrada.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao listar categorias: {err}")

    def adicionar_produto(self, nome, preco, desconto, id_categoria):
        try:
            query = "INSERT INTO produto (nome, preco, desconto, id_categoria) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (nome, preco, desconto, id_categoria))
            self.conexao.commit()
            print("✅ Produto adicionado com sucesso.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao adicionar produto: {err}")

    def listar_produtos(self):
        try:
            query = "SELECT sku, nome, preco, desconto, id_categoria FROM produto"
            self.cursor.execute(query)
            produtos = self.cursor.fetchall()
            if produtos:
                print("\n🛒 Produtos disponíveis:")
                for p in produtos:
                    print(f"SKU: {p[0]} - Nome: {p[1]} - Preço: €{p[2]:.2f} - Desconto: {p[3]}% - Categoria ID: {p[4]}")
            else:
                print("⚠️ Nenhum produto encontrado.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao listar produtos: {err}")

    def adicionar_ao_carrinho(self, id_produto, quantidade=1):
        try:
            query = "INSERT INTO carrinho (id_produto, quantidade) VALUES (%s, %s)"
            self.cursor.execute(query, (id_produto, quantidade))
            self.conexao.commit()
            print("✅ Produto adicionado ao carrinho.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao adicionar ao carrinho: {err}")

    def ver_carrinho(self):
        try:
            query = """
            SELECT c.id, p.nome, p.preco, p.desconto, c.quantidade,
                   (p.preco - (p.preco * p.desconto / 100)) * c.quantidade AS total
            FROM carrinho c
            JOIN produto p ON c.id_produto = p.sku
            """
            self.cursor.execute(query)
            itens = self.cursor.fetchall()
            if itens:
                print("\n🧾 Itens no carrinho:")
                for item in itens:
                    print(f"ID: {item[0]} - Produto: {item[1]} - Unitário: €{item[2]:.2f} - "
                          f"Desconto: {item[3]}% - Qtd: {item[4]} - Total: €{item[5]:.2f}")
            else:
                print("🛒 Carrinho vazio.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao visualizar carrinho: {err}")

    def remover_do_carrinho(self, id_item):
        try:
            query = "DELETE FROM carrinho WHERE id = %s"
            self.cursor.execute(query, (id_item,))
            self.conexao.commit()
            if self.cursor.rowcount > 0:
                print("✅ Item removido do carrinho.")
            else:
                print("⚠️ Item não encontrado.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao remover item do carrinho: {err}")

    def calcular_total(self):
        try:
            query = """
            SELECT SUM((p.preco - (p.preco * p.desconto / 100)) * c.quantidade)
            FROM carrinho c
            JOIN produto p ON c.id_produto = p.sku
            """
            self.cursor.execute(query)
            total = self.cursor.fetchone()[0]
            if total is not None:
                print(f"\n💰 Total a pagar: €{total:.2f}")
            else:
                print("🛒 Carrinho está vazio.")
        except mysql.connector.Error as err:
            print(f"❌ Erro ao calcular total: {err}")

    def fecharconexao(self):
        self.cursor.close()
        self.conexao.close()
        print("🔌 Conexão encerrada.")


def menu():
    carrinho = CarrinhodeCompras()
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Adicionar categoria")
        print("2. Listar categorias")
        print("3. Adicionar produto")
        print("4. Listar produtos")
        print("5. Adicionar ao carrinho")
        print("6. Ver carrinho")
        print("7. Remover item do carrinho")
        print("8. Calcular total")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome da nova categoria: ")
            carrinho.adicionar_categoria(nome)

        elif opcao == '2':
            carrinho.listar_categorias()

        elif opcao == '3':
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            desconto = float(input("Desconto (%): "))
            id_categoria = int(input("ID da categoria: "))
            carrinho.adicionar_produto(nome, preco, desconto, id_categoria)

        elif opcao == '4':
            carrinho.listar_produtos()

        elif opcao == '5':
            sku = int(input("Digite o SKU do produto: "))
            qtd = int(input("Quantidade: "))
            carrinho.adicionar_ao_carrinho(sku, qtd)

        elif opcao == '6':
            carrinho.ver_carrinho()

        elif opcao == '7':
            id_item = int(input("Digite o ID do item no carrinho a remover: "))
            carrinho.remover_do_carrinho(id_item)

        elif opcao == '8':
            carrinho.calcular_total()

        elif opcao == '9':
            carrinho.fecharconexao()
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()


