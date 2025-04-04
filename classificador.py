# classificador.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import matplotlib.pyplot as plt

# Função para treinar e avaliar os modelos de classificação
def executar_classificacao(df):
    # Seleção de variáveis para o modelo
    df['Categoria'] = df['Categoria'].astype('category').cat.codes  # Convertendo categorias em números
    df['Sexo'] = df['Sexo'].astype('category').cat.codes

    X = df[['Quantidade', 'Preço', 'Idade', 'Categoria', 'Sexo']]
    y = df['Produto'].apply(lambda x: 1 if x == 'Proteína Whey' else 0)  # Exemplo de classificação binária

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    modelos = {
        'Regressão Logística': LogisticRegression(),
        'k-NN': KNeighborsClassifier(),
        'Random Forest': RandomForestClassifier()
    }

    resultados = {}
    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='binary')
        rec = recall_score(y_test, y_pred, average='binary')
        f1 = f1_score(y_test, y_pred, average='binary')

        resultados[nome] = {'Acurácia': acc, 'Precisão': prec, 'Revocação': rec, 'F1-Score': f1}

        fpr, tpr, _ = roc_curve(y_test, modelo.predict_proba(X_test)[:, 1])
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos')
        plt.ylabel('Taxa de Verdadeiros Positivos')
        plt.title(f'Curva ROC - {nome}')
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(f'resultados/graficos/roc_{nome.lower().replace(" ", "_")}.png')
        plt.close()

    return resultados

if __name__ == "__main__":
    df = pd.read_csv('dados/vendas_suplementos.csv')
    resultados = executar_classificacao(df)
    print(resultados)