import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np

from carregador_dados import carregar_dados
from analise_dados import mostrar_analise
from classificador import executar_classificacao
from produto import GestorProdutos

class StoreAnalyzerDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("StoreAnalyzer - Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        self.df = None
        self.resultados_classificacao = None
        self.gestor_produtos = GestorProdutos()
        
        self.criar_interface()
        
    def criar_interface(self):
        frame_cabecalho = tk.Frame(self.root, bg="#4472C4", padx=10, pady=10)
        frame_cabecalho.pack(fill=tk.X)
        
        tk.Label(frame_cabecalho, text="StoreAnalyzer Dashboard", 
                font=("Arial", 18, "bold"), bg="#4472C4", fg="white").pack()
        
        self.tab_control = ttk.Notebook(self.root)
        
        self.tab_visao_geral = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_visao_geral, text="Visão Geral")
        
        self.tab_analise = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_analise, text="Análise Detalhada")
        
        self.tab_classificacao = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_classificacao, text="Classificação")
        
        self.tab_produtos = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_produtos, text="Gestão de Produtos")
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.configurar_tab_visao_geral()
        self.configurar_tab_analise()
        self.configurar_tab_classificacao()
        self.configurar_tab_produtos()
        
        self.status_bar = tk.Label(self.root, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.carregar_dados()
        
    def configurar_tab_visao_geral(self):
        frame = tk.Frame(self.tab_visao_geral, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        frame_resumo = tk.LabelFrame(frame, text="Resumo dos Dados", padx=10, pady=10)
        frame_resumo.pack(fill=tk.X, pady=10)
        
        self.lbl_total_vendas = tk.Label(frame_resumo, text="Total de Vendas: -")
        self.lbl_total_vendas.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.lbl_total_receita = tk.Label(frame_resumo, text="Receita Total: -")
        self.lbl_total_receita.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.lbl_produto_top = tk.Label(frame_resumo, text="Produto Mais Vendido: -")
        self.lbl_produto_top.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.lbl_regiao_top = tk.Label(frame_resumo, text="Região com Maior Receita: -")
        self.lbl_regiao_top.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.frame_graficos_resumo = tk.Frame(frame)
        self.frame_graficos_resumo.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def configurar_tab_analise(self):
        frame = tk.Frame(self.tab_analise, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        frame_controles = tk.Frame(frame)
        frame_controles.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_controles, text="Tipo de Gráfico:").pack(side=tk.LEFT, padx=5)
        self.combo_grafico = ttk.Combobox(frame_controles, 
                                          values=["Vendas por Produto", "Receita por Região", "Idades por Sexo"])
        self.combo_grafico.pack(side=tk.LEFT, padx=5)
        self.combo_grafico.current(0)
        
        tk.Button(frame_controles, text="Gerar Gráfico", 
                  command=self.gerar_grafico_analise).pack(side=tk.LEFT, padx=5)
        
        self.frame_grafico_analise = tk.Frame(frame)
        self.frame_grafico_analise.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def configurar_tab_classificacao(self):
        frame = tk.Frame(self.tab_classificacao, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        frame_controles = tk.Frame(frame)
        frame_controles.pack(fill=tk.X, pady=10)
        
        tk.Button(frame_controles, text="Executar Classificação", 
                  command=self.executar_classificacao).pack(side=tk.LEFT, padx=5)
        
        frame_resultados = tk.LabelFrame(frame, text="Resultados", padx=10, pady=10)
        frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tree_resultados = ttk.Treeview(frame_resultados, columns=("Modelo", "Acurácia", "Precisão", "Revocação", "F1"))
        self.tree_resultados.heading("#0", text="")
        self.tree_resultados.heading("Modelo", text="Modelo")
        self.tree_resultados.heading("Acurácia", text="Acurácia")
        self.tree_resultados.heading("Precisão", text="Precisão")
        self.tree_resultados.heading("Revocação", text="Revocação")
        self.tree_resultados.heading("F1", text="F1-Score")
        
        self.tree_resultados.column("#0", width=0, stretch=tk.NO)
        self.tree_resultados.column("Modelo", width=150)
        self.tree_resultados.column("Acurácia", width=100)
        self.tree_resultados.column("Precisão", width=100)
        self.tree_resultados.column("Revocação", width=100)
        self.tree_resultados.column("F1", width=100)
        
        self.tree_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.frame_roc_curves = tk.Frame(frame)
        self.frame_roc_curves.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def configurar_tab_produtos(self):
        frame = tk.Frame(self.tab_produtos, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        frame_lista = tk.LabelFrame(frame, text="Lista de Produtos", padx=10, pady=10)
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        frame_tools = tk.Frame(frame_lista)
        frame_tools.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(frame_tools, text="Novo Produto", command=self.abrir_form_novo_produto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Editar", command=self.editar_produto_selecionado).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Remover", command=self.remover_produto_selecionado).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Atualizar", command=self.atualizar_lista_produtos).pack(side=tk.LEFT, padx=5)
        
        colunas = ("ID", "Nome", "Categoria", "Preço", "Stock")
        self.tree_produtos = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_produtos.heading(col, text=col)
            width = 70 if col in ("ID", "Preço", "Stock") else 150
            self.tree_produtos.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_produtos.pack(fill=tk.BOTH, expand=True)
        
        self.tree_produtos.bind("<Double-1>", lambda event: self.editar_produto_selecionado())
        
        self.frame_detalhes = tk.LabelFrame(frame, text="Detalhes do Produto", padx=10, pady=10)
        self.frame_detalhes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        campos = [
            ("ID:", "entry_id", True),
            ("Nome:", "entry_nome", False),
            ("Categoria:", "combo_categoria", False),
            ("Preço Base:", "entry_preco", False),
            ("Stock:", "entry_stock", False),
            ("Descrição:", "text_descricao", False)
        ]
        
        for i, (label_text, campo_nome, somente_leitura) in enumerate(campos):
            frame_campo = tk.Frame(self.frame_detalhes)
            frame_campo.pack(fill=tk.X, pady=5)
            
            tk.Label(frame_campo, text=label_text, width=10, anchor="w").pack(side=tk.LEFT)
            
            if campo_nome == "combo_categoria":
                categorias = self.gestor_produtos.obter_categorias() or ["Ganhos Musculares", "Energia", "Recuperação", "Saúde"]
                setattr(self, campo_nome, ttk.Combobox(frame_campo, values=categorias))
                getattr(self, campo_nome).pack(side=tk.LEFT, fill=tk.X, expand=True)
            elif campo_nome == "text_descricao":
                setattr(self, campo_nome, tk.Text(frame_campo, height=5, width=30))
                getattr(self, campo_nome).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            else:
                setattr(self, campo_nome, tk.Entry(frame_campo))
                getattr(self, campo_nome).pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                if somente_leitura:
                    getattr(self, campo_nome).config(state="readonly")
        
        frame_botoes = tk.Frame(self.frame_detalhes)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        tk.Button(frame_botoes, text="Guardar", command=self.guardar_produto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        self.atualizar_lista_produtos()
        self.limpar_formulario()
    
    def atualizar_lista_produtos(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        produtos_df = self.gestor_produtos.obter_todos_produtos()
        
        if produtos_df is not None and not produtos_df.empty:
            for idx, row in produtos_df.iterrows():
                self.tree_produtos.insert("", tk.END, values=(
                    row['ID'],
                    row['Nome'],
                    row['Categoria'],
                    f"{row['Preço_Base']:.2f} €",
                    row['Stock']
                ))
    
    def limpar_formulario(self):
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        
        self.entry_nome.delete(0, tk.END)
        
        categorias = self.gestor_produtos.obter_categorias() or ["Ganhos Musculares", "Energia", "Recuperação", "Saúde"]
        self.combo_categoria.config(values=categorias)
        self.combo_categoria.delete(0, tk.END)
        
        self.entry_preco.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        
        self.frame_detalhes.config(text="Detalhes do Produto")
    
    def abrir_form_novo_produto(self):
        self.limpar_formulario()
        self.frame_detalhes.config(text="Novo Produto")
    
    def editar_produto_selecionado(self):
        selection = self.tree_produtos.selection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        
        produto = self.gestor_produtos.obter_produto(produto_id)
        
        if not produto:
            messagebox.showerror("Erro", "Não foi possível obter os detalhes do produto")
            return
        
        self.limpar_formulario()
        
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, produto['ID'])
        self.entry_id.config(state="readonly")
        
        self.entry_nome.insert(0, produto['Nome'])
        self.combo_categoria.set(produto['Categoria'])
        self.entry_preco.insert(0, produto['Preço_Base'])
        self.entry_stock.insert(0, produto['Stock'])
        self.text_descricao.insert("1.0", produto['Descrição'])
        
        self.frame_detalhes.config(text=f"Editar Produto: {produto['Nome']}")
    
    def remover_produto_selecionado(self):
        selection = self.tree_produtos.selection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para remover")
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        produto_nome = item['values'][1]
        
        confirmar = messagebox.askyesno("Confirmar", f"Deseja realmente remover o produto '{produto_nome}'?")
        
        if confirmar:
            if self.gestor_produtos.remover_produto(produto_id):
                messagebox.showinfo("Sucesso", f"Produto '{produto_nome}' removido com sucesso")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
    
    def guardar_produto(self):
        produto_id = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get().strip()
        preco_base = self.entry_preco.get().strip()
        stock = self.entry_stock.get().strip()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome do produto é obrigatório")
            return
        
        if not categoria:
            messagebox.showwarning("Aviso", "A categoria é obrigatória")
            return
        
        try:
            preco_base = float(preco_base)
            if preco_base <= 0:
                raise ValueError("O preço deve ser maior que zero")
        except ValueError:
            messagebox.showwarning("Aviso", "O preço base deve ser um número válido maior que zero")
            return
        
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError("O stock não pode ser negativo")
        except ValueError:
            messagebox.showwarning("Aviso", "O stock deve ser um número inteiro não negativo")
            return
        
        if produto_id:
            if self.gestor_produtos.atualizar_produto(int(produto_id), nome, categoria, preco_base, stock, descricao):
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
        else:
            sucesso, novo_id = self.gestor_produtos.adicionar_produto(nome, categoria, preco_base, stock, descricao)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso (ID: {novo_id})")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
    
    def carregar_dados(self):
        self.atualizar_status("A carregar dados...")
        self.df = carregar_dados()
        
        if self.df is not None:
            self.atualizar_status("Dados carregados com sucesso!")
            self.atualizar_visao_geral()
        else:
            self.atualizar_status("Erro ao carregar dados.")
            messagebox.showerror("Erro", "Não foi possível carregar os dados.")
    
    def atualizar_visao_geral(self):
        if self.df is None:
            return
            
        self.df['Receita'] = self.df['Quantidade'] * self.df['Preço']
        total_vendas = self.df['Quantidade'].sum()
        total_receita = self.df['Receita'].sum()
        produto_top = self.df.groupby('Produto')['Quantidade'].sum().idxmax()
        regiao_top = self.df.groupby('Região')['Receita'].sum().idxmax()
        
        self.lbl_total_vendas.config(text=f"Total de Vendas: {total_vendas}")
        self.lbl_total_receita.config(text=f"Receita Total: {total_receita:.2f} €")
        self.lbl_produto_top.config(text=f"Produto Mais Vendido: {produto_top}")
        self.lbl_regiao_top.config(text=f"Região com Maior Receita: {regiao_top}")
        
        for widget in self.frame_graficos_resumo.winfo_children():
            widget.destroy()
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        self.df.groupby('Produto')['Quantidade'].sum().sort_values().plot(
            kind='barh', ax=ax1, title="Vendas por Produto")
        ax1.set_xlabel("Quantidade")
        
        self.df.groupby('Região')['Receita'].sum().plot(
            kind='bar', ax=ax2, color='orange', title="Receita por Região")
        ax2.set_ylabel("Receita (€)")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.frame_graficos_resumo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def gerar_grafico_analise(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado.")
            return
            
        for widget in self.frame_grafico_analise.winfo_children():
            widget.destroy()
            
        tipo_grafico = self.combo_grafico.get()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if tipo_grafico == "Vendas por Produto":
            self.df.groupby('Produto')['Quantidade'].sum().sort_values().plot(
                kind='barh', ax=ax, title="Total de Vendas por Produto")
            ax.set_xlabel("Quantidade")
            
        elif tipo_grafico == "Receita por Região":
            self.df.groupby('Região')['Receita'].sum().plot(
                kind='bar', ax=ax, color='orange', title="Receita por Região")
            ax.set_ylabel("Receita (€)")
            
        elif tipo_grafico == "Idades por Sexo":
            for sexo in ['Masculino', 'Feminino']:
                self.df[self.df['Sexo'] == sexo]['Idade'].plot(
                    kind='hist', alpha=0.5, label=sexo, ax=ax)
            ax.set_title('Distribuição de Idades por Sexo')
            ax.legend()
            
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_analise)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def executar_classificacao(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado.")
            return
            
        self.atualizar_status("A executar classificação...")
        
        os.makedirs('resultados/graficos', exist_ok=True)
        
        self.resultados_classificacao = executar_classificacao(self.df)
        
        for item in self.tree_resultados.get_children():
            self.tree_resultados.delete(item)
            
        for modelo, metricas in self.resultados_classificacao.items():
            self.tree_resultados.insert("", tk.END, values=(
                modelo,
                f"{metricas['Acurácia']:.4f}",
                f"{metricas['Precisão']:.4f}",
                f"{metricas['Revocação']:.4f}",
                f"{metricas['F1-Score']:.4f}"
            ))
            
        self.mostrar_curvas_roc()
        
        self.atualizar_status("Classificação concluída!")
    
    def mostrar_curvas_roc(self):
        for widget in self.frame_roc_curves.winfo_children():
            widget.destroy()
            
        frame_imgs = tk.Frame(self.frame_roc_curves)
        frame_imgs.pack(fill=tk.BOTH, expand=True)
        
        modelos = ['regressão_logística', 'k-nn', 'random_forest']
        labels = ['Regressão Logística', 'k-NN', 'Random Forest']
        
        for i, (modelo, label) in enumerate(zip(modelos, labels)):
            img_path = f'resultados/graficos/roc_{modelo}.png'
            if os.path.exists(img_path):
                img_frame = tk.LabelFrame(frame_imgs, text=label, padx=5, pady=5)
                img_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
                
                from PIL import Image, ImageTk
                img = Image.open(img_path)
                img = img.resize((300, 240), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                
                img_frame.image = img_tk
                
                lbl_img = tk.Label(img_frame, image=img_tk)
                lbl_img.pack(fill=tk.BOTH, expand=True)
                
        frame_imgs.columnconfigure(0, weight=1)
        frame_imgs.columnconfigure(1, weight=1)
        frame_imgs.columnconfigure(2, weight=1)
    
    def atualizar_status(self, mensagem):
        self.status_bar.config(text=mensagem)
        self.root.update_idletasks()

def iniciar_dashboard():
    root = tk.Tk()
    app = StoreAnalyzerDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_dashboard()