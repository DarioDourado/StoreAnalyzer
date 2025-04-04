import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class GestorProdutos:
    def __init__(self):
        self.produtos_df = None
        self.caminho_produtos = "dados/produtos.csv"
        self.carregar_produtos()
    
    def carregar_produtos(self):
        """Carrega produtos do CSV ou cria um novo se não existir"""
        if os.path.exists(self.caminho_produtos):
            try:
                self.produtos_df = pd.read_csv(self.caminho_produtos)
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
                return False
        else:
            # Criar ficheiro de produtos inicial
            self.produtos_df = pd.DataFrame({
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
            self.guardar_produtos()
            return True
    
    def guardar_produtos(self):
        """Guarda os produtos no ficheiro CSV"""
        try:
            os.makedirs(os.path.dirname(self.caminho_produtos), exist_ok=True)
            self.produtos_df.to_csv(self.caminho_produtos, index=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar produtos: {e}")
            return False
    
    def adicionar_produto(self, nome, categoria, preco_base, stock, descricao):
        """Adiciona um novo produto"""
        try:
            # Determinar o próximo ID
            proximo_id = 1
            if not self.produtos_df.empty:
                proximo_id = self.produtos_df['ID'].max() + 1
            
            # Adicionar o novo produto
            novo_produto = pd.DataFrame({
                'ID': [proximo_id],
                'Nome': [nome],
                'Categoria': [categoria],
                'Preço_Base': [float(preco_base)],
                'Stock': [int(stock)],
                'Descrição': [descricao]
            })
            
            self.produtos_df = pd.concat([self.produtos_df, novo_produto], ignore_index=True)
            self.guardar_produtos()
            return True, proximo_id
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")
            return False, None
    
    def atualizar_produto(self, id_produto, nome, categoria, preco_base, stock, descricao):
        """Atualiza um produto existente"""
        try:
            if id_produto not in self.produtos_df['ID'].values:
                messagebox.showerror("Erro", f"Produto com ID {id_produto} não encontrado")
                return False
            
            # Localizar o índice do produto no DataFrame
            idx = self.produtos_df[self.produtos_df['ID'] == id_produto].index[0]
            
            # Atualizar os valores
            self.produtos_df.at[idx, 'Nome'] = nome
            self.produtos_df.at[idx, 'Categoria'] = categoria
            self.produtos_df.at[idx, 'Preço_Base'] = float(preco_base)
            self.produtos_df.at[idx, 'Stock'] = int(stock)
            self.produtos_df.at[idx, 'Descrição'] = descricao
            
            self.guardar_produtos()
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
            return False
    
    def remover_produto(self, id_produto):
        """Remove um produto pelo ID"""
        try:
            if id_produto not in self.produtos_df['ID'].values:
                messagebox.showerror("Erro", f"Produto com ID {id_produto} não encontrado")
                return False
            
            # Remover o produto
            self.produtos_df = self.produtos_df[self.produtos_df['ID'] != id_produto]
            self.guardar_produtos()
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover produto: {e}")
            return False
    
    def obter_produto(self, id_produto):
        """Obtém os detalhes de um produto pelo ID"""
        try:
            produto = self.produtos_df[self.produtos_df['ID'] == id_produto]
            if produto.empty:
                return None
            return produto.iloc[0].to_dict()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter produto: {e}")
            return None
    
    def obter_todos_produtos(self):
        """Retorna todos os produtos"""
        return self.produtos_df
    
    def obter_categorias(self):
        """Retorna todas as categorias únicas"""
        return self.produtos_df['Categoria'].unique().tolist()