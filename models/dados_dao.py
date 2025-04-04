import pandas as pd
import os

class DadosDAO:
    """Data Access Object para operações com dados de análise"""
    
    def __init__(self, caminho_vendas="dados/vendas_suplementos.csv"):
        self.caminho_vendas = caminho_vendas
    
    def carregar_dados_vendas(self):
        """Carrega dados de vendas do CSV ou cria um exemplo se não existir"""
        try:
            if os.path.exists(self.caminho_vendas):
                return pd.read_csv(self.caminho_vendas)
            else:
                # Criar dados de exemplo
                return self._criar_dados_exemplo()
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None
    
    def _criar_dados_exemplo(self):
        """Cria um conjunto de dados de exemplo para demonstração"""
        import numpy as np
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.caminho_vendas), exist_ok=True)
        
        # Produtos disponíveis
        produtos = ["Proteína Whey", "Creatina", "BCAA", "Pré-treino", "Vitaminas", "Omega 3"]
        categorias = {
            "Proteína Whey": 1, "Creatina": 1, "BCAA": 2, "Pré-treino": 3, "Vitaminas": 4, "Omega 3": 4
        }
        regioes = ["Norte", "Centro", "Sul", "Ilhas"]
        sexos = ["Masculino", "Feminino"]
        
        # Gerar dados aleatórios
        n_registros = 500
        np.random.seed(42)  # Para reproduzibilidade
        
        data = {
            'ID_Venda': np.arange(1, n_registros + 1),
            'Data': pd.date_range(start='2024-01-01', periods=n_registros).strftime('%Y-%m-%d'),
            'Produto': np.random.choice(produtos, size=n_registros, p=[0.3, 0.2, 0.15, 0.15, 0.1, 0.1]),
            'Quantidade': np.random.randint(1, 5, size=n_registros),
            'Preço': np.random.uniform(15, 50, size=n_registros).round(2),
            'Cliente_ID': np.random.randint(1, 101, size=n_registros),
            'Idade': np.random.randint(18, 65, size=n_registros),
            'Sexo': np.random.choice(sexos, size=n_registros),
            'Região': np.random.choice(regioes, size=n_registros)
        }
        
        # Adicionar categoria baseada no produto
        data['Categoria'] = [categorias[produto] for produto in data['Produto']]
        
        # Criar DataFrame
        df = pd.DataFrame(data)
        
        # Salvar para uso futuro
        df.to_csv(self.caminho_vendas, index=False)
        
        return df