import pandas as pd
import os
from tkinter import messagebox

def carregar_dados(caminho="dados/vendas_suplementos.csv"):
    if not os.path.exists(caminho):
        messagebox.showerror("Erro", f"Ficheiro não encontrado: {caminho}")
        return None

    try:
        df = pd.read_csv(caminho)

        obrigatorias = ['ID', 'Produto', 'Categoria', 'Quantidade', 'Preço', 'Cliente', 'Sexo', 'Idade', 'Região', 'Data']
        for col in obrigatorias:
            if col not in df.columns:
                messagebox.showerror("Erro", f"Coluna em falta: {col}")
                return None

        df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce')
        df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
        df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df = df.dropna()

        return df

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
        return None