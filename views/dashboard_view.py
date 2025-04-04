import tkinter as tk
from tkinter import ttk, messagebox
import os
from controllers.analise_controller import AnaliseController
from controllers.classificacao_controller import ClassificacaoController

class DashboardView(ttk.Frame):
    """View principal para o dashboard de análise"""
    
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.analise_controller = AnaliseController()
        self.classificacao_controller = ClassificacaoController()
        self.create_widgets()
    
    def create_widgets(self):
        # Criar notebook para subseções do dashboard
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Adicionar tabs
        self.tab_visao_geral = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_visao_geral, text="Visão Geral")
        
        self.tab_analise = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_analise, text="Análise Detalhada")
        
        self.tab_classificacao = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_classificacao, text="Classificação")
        
        # Configurar cada tab
        self.configurar_tab_visao_geral()
        self.configurar_tab_analise()
        self.configurar_tab_classificacao()
        
        # Status bar
        self.status_bar = tk.Label(self, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Carregar dados iniciais
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
    
    def carregar_dados(self):
        self.atualizar_status("A carregar dados...")
        
        try:
            self.df = self.analise_controller.carregar_dados()
            
            if self.df is not None:
                self.atualizar_status("Dados carregados com sucesso!")
                self.atualizar_visao_geral()
            else:
                self.atualizar_status("Erro ao carregar dados.")
                messagebox.showerror("Erro", "Não foi possível carregar os dados.")
        except Exception as e:
            self.atualizar_status(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def atualizar_visao_geral(self):
        if self.df is None:
            return
            
        resumo = self.analise_controller.gerar_resumo(self.df)
        
        self.lbl_total_vendas.config(text=f"Total de Vendas: {resumo['total_vendas']}")
        self.lbl_total_receita.config(text=f"Receita Total: {resumo['total_receita']:.2f} €")
        self.lbl_produto_top.config(text=f"Produto Mais Vendido: {resumo['produto_top']}")
        self.lbl_regiao_top.config(text=f"Região com Maior Receita: {resumo['regiao_top']}")
        
        for widget in self.frame_graficos_resumo.winfo_children():
            widget.destroy()
            
        self.analise_controller.gerar_graficos_resumo(self.df, self.frame_graficos_resumo)
    
    def gerar_grafico_analise(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado.")
            return
            
        for widget in self.frame_grafico_analise.winfo_children():
            widget.destroy()
            
        tipo_grafico = self.combo_grafico.get()
        self.analise_controller.gerar_grafico_especifico(self.df, tipo_grafico, self.frame_grafico_analise)
    
    def executar_classificacao(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado.")
            return
            
        self.atualizar_status("A executar classificação...")
        
        os.makedirs('resultados/graficos', exist_ok=True)
        
        try:
            self.resultados_classificacao = self.classificacao_controller.executar_classificacao(self.df)
            
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
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na classificação: {str(e)}")
            self.atualizar_status(f"Erro: {str(e)}")
    
    def mostrar_curvas_roc(self):
        for widget in self.frame_roc_curves.winfo_children():
            widget.destroy()
            
        try:
            self.classificacao_controller.mostrar_curvas_roc(self.frame_roc_curves)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar curvas ROC: {str(e)}")
    
    def atualizar_status(self, mensagem):
        self.status_bar.config(text=mensagem)
        self.parent.update_idletasks()