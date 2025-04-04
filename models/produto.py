class Produto:
    """Classe que representa a entidade Produto"""
    
    def __init__(self, id=None, nome="", categoria="", preco_base=0.0, stock=0, descricao=""):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco_base = preco_base
        self.stock = stock
        self.descricao = descricao
    
    def to_dict(self):
        """Converte objeto para dicionário"""
        return {
            'ID': self.id,
            'Nome': self.nome,
            'Categoria': self.categoria,
            'Preço_Base': self.preco_base,
            'Stock': self.stock,
            'Descrição': self.descricao
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria objeto a partir de dicionário"""
        return cls(
            id=data.get('ID'),
            nome=data.get('Nome'),
            categoria=data.get('Categoria'),
            preco_base=data.get('Preço_Base'),
            stock=data.get('Stock'),
            descricao=data.get('Descrição')
        )