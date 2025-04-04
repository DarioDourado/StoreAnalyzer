from models.produto import Produto
from models.produto_dao import ProdutoDAO

class ProdutoController:
    """Controlador para a entidade Produto"""
    
    def __init__(self):
        self.dao = ProdutoDAO()
    
    def listar_todos(self):
        """Retorna todos os produtos"""
        return self.dao.obter_todos()
    
    def obter_produto(self, produto_id):
        """Obtém os detalhes de um produto pelo ID"""
        return self.dao.obter_produto(produto_id)
    
    def adicionar_produto(self, nome, categoria, preco_base, stock, descricao):
        """Adiciona um novo produto"""
        try:
            # Validações
            if not nome or not categoria:
                return False, "Nome e categoria são obrigatórios"
            
            preco_base = float(preco_base)
            if preco_base <= 0:
                return False, "Preço deve ser maior que zero"
            
            stock = int(stock)
            if stock < 0:
                return False, "Stock não pode ser negativo"
            
            # Criar objeto Produto
            produto = Produto(
                nome=nome,
                categoria=categoria,
                preco_base=preco_base,
                stock=stock,
                descricao=descricao
            )
            
            # Adicionar via DAO
            sucesso, produto_id = self.dao.adicionar(produto)
            if sucesso:
                return True, produto_id
            else:
                return False, "Erro ao adicionar produto"
            
        except ValueError:
            return False, "Valores inválidos para preço ou stock"
        except Exception as e:
            return False, str(e)
    
    def atualizar_produto(self, produto_id, nome, categoria, preco_base, stock, descricao):
        """Atualiza um produto existente"""
        try:
            # Validações
            if not nome or not categoria:
                return False, "Nome e categoria são obrigatórios"
            
            preco_base = float(preco_base)
            if preco_base <= 0:
                return False, "Preço deve ser maior que zero"
            
            stock = int(stock)
            if stock < 0:
                return False, "Stock não pode ser negativo"
            
            # Criar objeto Produto
            produto = Produto(
                id=produto_id,
                nome=nome,
                categoria=categoria,
                preco_base=preco_base,
                stock=stock,
                descricao=descricao
            )
            
            # Atualizar via DAO
            sucesso = self.dao.atualizar(produto)
            if sucesso:
                return True, "Produto atualizado com sucesso"
            else:
                return False, "Erro ao atualizar produto"
            
        except ValueError:
            return False, "Valores inválidos para preço ou stock"
        except Exception as e:
            return False, str(e)
    
    def remover_produto(self, produto_id):
        """Remove um produto pelo ID"""
        try:
            sucesso = self.dao.remover(produto_id)
            if sucesso:
                return True, "Produto removido com sucesso"
            else:
                return False, "Produto não encontrado"
        except Exception as e:
            return False, str(e)
    
    def obter_categorias(self):
        """Retorna todas as categorias únicas"""
        return self.dao.obter_categorias()