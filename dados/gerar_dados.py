# gerar_dados.py
import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_dados():
    produtos = ["Proteína Whey", "Creatina", "BCAA", "Pré-treino", "Vitaminas", "Omega 3"]
    categorias = ["Ganhos Musculares", "Energia", "Recuperação", "Saúde"]
    regioes = ["Norte", "Centro", "Sul", "Ilhas"]
    sexos = ["Masculino", "Feminino"]

    dados = []

    for i in range(1, 101):
        produto = random.choice(produtos)
        categoria = random.choice(categorias)
        quantidade = random.randint(1, 5)
        preco = round(random.uniform(10, 80), 2)
        cliente = f"Cliente_{i}"
        sexo = random.choice(sexos)
        idade = random.randint(18, 60)
        regiao = random.choice(regioes)
        data = datetime.today() - timedelta(days=random.randint(0, 365))

        dados.append([i, produto, categoria, quantidade, preco, cliente, sexo, idade, regiao, data.date()])

    colunas = ['ID', 'Produto', 'Categoria', 'Quantidade', 'Preço', 'Cliente', 'Sexo', 'Idade', 'Região', 'Data']
    df = pd.DataFrame(dados, columns=colunas)
    df.to_csv("dados/vendas_suplementos.csv", index=False)
    print("✔️ Ficheiro 'vendas_suplementos.csv' gerado com sucesso.")

if __name__ == "__main__":
    gerar_dados()
