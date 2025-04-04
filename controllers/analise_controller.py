import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from models.dados_dao import DadosDAO

class AnaliseController:
    """Controlador para análise de dados"""
    
    def __init__(self):
        self.dados_dao = DadosDAO()
    
    def carregar_dados(self):
        """Carrega os dados para análise"""
        return self.dados_dao.carregar_dados_vendas()
    
    def gerar_resumo(self, df):
        """Gera um resumo estatístico dos dados"""
        df['Receita'] = df['Quantidade'] * df['Preço']
        
        resumo = {
            'total_vendas': df['Quantidade'].sum(),
            'total_receita': df['Receita'].sum(),
            'produto_top': df.groupby('Produto')['Quantidade'].sum().idxmax(),
            'regiao_top': df.groupby('Região')['Receita'].sum().idxmax()
        }
        
        return resumo
    
    def gerar_graficos_resumo(self, df, frame):
        """Gera gráficos de resumo para a visão geral"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        df.groupby('Produto')['Quantidade'].sum().sort_values().plot(
            kind='barh', ax=ax1, title="Vendas por Produto")
        ax1.set_xlabel("Quantidade")
        
        df.groupby('Região')['Receita'].sum().plot(
            kind='bar', ax=ax2, color='orange', title="Receita por Região")
        ax2.set_ylabel("Receita (€)")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def gerar_grafico_especifico(self, df, tipo_grafico, frame):
        """Gera um gráfico específico com base no tipo selecionado"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if tipo_grafico == "Vendas por Produto":
            df.groupby('Produto')['Quantidade'].sum().sort_values().plot(
                kind='barh', ax=ax, title="Total de Vendas por Produto")
            ax.set_xlabel("Quantidade")
            
        elif tipo_grafico == "Receita por Região":
            df.groupby('Região')['Receita'].sum().plot(
                kind='bar', ax=ax, color='orange', title="Receita por Região")
            ax.set_ylabel("Receita (€)")
            
        elif tipo_grafico == "Idades por Sexo":
            for sexo in ['Masculino', 'Feminino']:
                df[df['Sexo'] == sexo]['Idade'].plot(
                    kind='hist', alpha=0.5, label=sexo, ax=ax)
            ax.set_title('Distribuição de Idades por Sexo')
            ax.legend()
            
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)