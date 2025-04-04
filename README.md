# StoreAnalyzer

## Descrição

StoreAnalyzer é uma aplicação desktop para análise de dados de vendas e gestão de produtos de uma loja de suplementos. Desenvolvida em Python, utiliza Tkinter para a interface gráfica e oferece funcionalidades de visualização de dados, classificação com machine learning e gestão completa de produtos.

## Características

- **Dashboard Interativo**: Visualização resumida de métricas de vendas e receitas
- **Análise Detalhada**: Gráficos e estatísticas sobre vendas por produto, região e perfil de clientes
- **Classificação com Machine Learning**: Predição de padrões de compra usando algoritmos como:
  - Regressão Logística
  - k-NN (k-Nearest Neighbors)
  - Random Forest
- **Gestão de Produtos (CRUD)**:
  - Cadastro de novos produtos
  - Visualização em lista
  - Edição de detalhes
  - Remoção de produtos

## Requisitos

- Python 3.8+
- Bibliotecas Python (listadas no arquivo requirements.txt):
  - pandas
  - scikit-learn
  - matplotlib
  - numpy
  - pillow

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/DarioDourado/StoreAnalyzer.git
   cd StoreAnalyzer
   ```

## Instalação dependências

pip install -r requirements.txt

## Execute o programa principal;

python main.py

## Desenvolvimento

O projeto segue uma arquitetura modular onde cada componente tem uma responsabilidade definida:

## Interface gráfica separada da lógica de negócios

Classes especializadas para cada funcionalidade
Persistência de dados em arquivos CSV
Análise com pandas e visualização com matplotlib

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Dario Dourado
