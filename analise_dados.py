import matplotlib.pyplot as plt

def mostrar_analise(df):
    df['Receita'] = df['Quantidade'] * df['Preço']

    df.groupby('Produto')['Quantidade'].sum().sort_values().plot(kind='barh', figsize=(10, 5), title="Total de Vendas por Produto")
    plt.tight_layout()
    plt.savefig("resultados/graficos/vendas_por_produto.png")
    plt.show()

    # Receita por Região
    df.groupby('Região')['Receita'].sum().plot(kind='bar', color='orange', figsize=(8, 5), title="Receita por Região")
    plt.tight_layout()
    plt.savefig("resultados/graficos/receita_por_regiao.png")
    plt.show()

    # Idades por Sexo
    df[df['Sexo'].isin(['Masculino', 'Feminino'])].groupby('Sexo')['Idade'].plot(kind='hist', alpha=0.5, legend=True)
    plt.title('Distribuição de Idades por Sexo')
    plt.tight_layout()
    plt.savefig("resultados/graficos/idades_por_sexo.png")
    plt.show()