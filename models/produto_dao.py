import os
import pandas as pd
from models.produto import Produto

class ProdutoDAO:
    """Data Access Object para Produtos"""
    
    def __init__(self, caminho_produtos="dados/produtos.csv"):
        self.caminho_produtos = caminho_produtos
        self.produtos_df = self._load_or_create_df()
    
    def _load_or_create_df(self):
        """Carrega o DataFrame de produtos ou cria um novo se não existir"""
        if os.path.exists(self.caminho_produtos):
            try:
                return pd.read_csv(self.caminho_produtos)
            except Exception as e:
                print(f"Erro ao carregar produtos: {e}")
                return self._criar_df_padrao()
        else:
            return self._criar_df_padrao()
    
    def _criar_df_padrao(self):
        """Cria DataFrame padrão com produtos iniciais"""
        df = pd.DataFrame({
            'ID': range(1, 7),
            'Nome': ["Proteína Whey", "Creatina", "BCAA", "Pré-treino", "Vitaminas", "Omega 3"],
            'Categoria': ["Ganhos Musculares", "Ganhos Musculares", "Recuperação", 
                         "Energia", "Saúde", "Saúde"],
            'Preço_Base': [45.99, 30.50, 25.00, 35.00, 20.00, 15.00],
            'Stock': [100, 150, 200, 80, 120, 90],
            'Descrição': [
                "Proteína para ganhos musculares", 
                "Suplemento para força muscular",
                "Aminoácidos para recuperação",
                "Energia para treinos intensos",
                "Multivitamínico diário",
                "Ácidos gordos essenciais"
            ]
        })
        self.guardar_produtos(df)
        return df
    
    def guardar_produtos(self, df=None):
        """Guarda os produtos no ficheiro CSV"""
        try:
            if df is None:
                df = self.produtos_df
            os.makedirs(os.path.dirname(self.caminho_produtos), exist_ok=True)
            df.to_csv(self.caminho_produtos, index=False)
            return True
        except Exception as e:
            print(f"Erro ao guardar produtos: {e}")
            return False
    
    def obter_todos(self):
        """Retorna todos os produtos como objetos Produto"""
        produtos = []
        for _, row in self.produtos_df.iterrows():
            produtos.append(Produto.from_dict(row))
        return produtos
    
    def obter_produto(self, produto_id):
        """Obtém um produto pelo ID"""
        produto = self.produtos_df[self.produtos_df['ID'] == produto_id]
        if produto.empty:
            return None
        return Produto.from_dict(produto.iloc[0])
    
    def adicionar(self, produto):
        """Adiciona um novo produto"""
        try:
            # Determinar o próximo ID
            proximo_id = 1
            if not self.produtos_df.empty:
                proximo_id = self.produtos_df['ID'].max() + 1
            
            # Definir ID se não estiver definido
            if produto.id is None:
                produto.id = proximo_id
            
            # Converter para DataFrame e concatenar
            produto_dict = produto.to_dict()
            novo_produto = pd.DataFrame([produto_dict])
            
            self.produtos_df = pd.concat([self.produtos_df, novo_produto], ignore_index=True)
            self.guardar_produtos()
            return True, produto.id
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return False, None
    
    def atualizar(self, produto):
        """Atualiza um produto existente"""
        try:
            if produto.id not in self.produtos_df['ID'].values:
                print(f"Produto com ID {produto.id} não encontrado")
                return False
            
            # Localizar o índice do produto no DataFrame
            idx = self.produtos_df[self.produtos_df['ID'] == produto.id].index[0]
            
            # Atualizar os valores
            produto_dict = produto.to_dict()
            for key, value in produto_dict.items():
                self.produtos_df.at[idx, key] = value
            
            self.guardar_produtos()
            return True
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            return False
    
    def remover(self, produto_id):
        """Remove um produto pelo ID"""
        try:
            if produto_id not in self.produtos_df['ID'].values:
                print(f"Produto com ID {produto_id} não encontrado")
                return False
            
            # Remover o produto
            self.produtos_df = self.produtos_df[self.produtos_df['ID'] != produto_id]
            self.guardar_produtos()
            return True
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            return False
    
    def obter_categorias(self):
        """Retorna todas as categorias únicas"""
        return self.produtos_df['Categoria'].unique().tolist()