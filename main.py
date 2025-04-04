import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import logging
from datetime import datetime
from views.produto_view import ProdutoView
from views.dashboard_view import DashboardView

# Configuração de logging
def configurar_logging():
    """Configura o sistema de logging da aplicação"""
    os.makedirs('logs', exist_ok=True)
    log_file = f'logs/storeanalyzer_{datetime.now().strftime("%Y%m%d")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('StoreAnalyzer')

# Handler global de exceções
def handler_excecao(tipo, valor, traceback):
    """Handler global para exceções não tratadas"""
    logger.error(f"Exceção não tratada: {tipo.__name__}: {valor}")
    messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {valor}\n\nConsulte os logs para mais detalhes.")
    sys.__excepthook__(tipo, valor, traceback)  # Chama o handler original para logging

# Garantir que diretórios necessários existam
def criar_diretorios():
    """Cria os diretórios necessários para a aplicação"""
    diretorios = ['dados', 'resultados/graficos']
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        logger.info(f"Diretório verificado/criado: {diretorio}")

# Configurar tema visual
def configurar_tema(root):
    """Configura o tema visual da aplicação"""
    style = ttk.Style(root)
    
    # Tente usar um tema mais moderno se disponível
    temas_disponiveis = style.theme_names()
    tema_escolhido = 'clam'  # tema base
    
    if 'vista' in temas_disponiveis:
        tema_escolhido = 'vista'
    elif 'winnative' in temas_disponiveis:
        tema_escolhido = 'winnative'
    
    style.theme_use(tema_escolhido)
    logger.info(f"Tema visual configurado: {tema_escolhido}")
    
    # Personalizações adicionais
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 10))
    style.configure('TButton', font=('Helvetica', 10))
    
    # Cores para TreeView
    style.configure('Treeview', 
                   background='#f8f8f8',
                   fieldbackground='#f8f8f8',
                   font=('Helvetica', 9))
    style.map('Treeview', background=[('selected', '#0078d7')])

def iniciar_app():
    """Inicializa a aplicação principal"""
    logger.info("Iniciando aplicação StoreAnalyzer")
    
    try:
        # Criar diretórios necessários
        criar_diretorios()
        
        # Configurar janela principal
        root = tk.Tk()
        root.title("StoreAnalyzer")
        root.geometry("1200x800")
        root.minsize(800, 600)  # Tamanho mínimo para usabilidade
        
        # Configurar tema visual
        configurar_tema(root)
        
        # Criar notebook (tabs)
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Adicionar tab de dashboard
        logger.info("Carregando módulo Dashboard")
        tab_dashboard = DashboardView(notebook)
        notebook.add(tab_dashboard, text="Dashboard")
        
        # Adicionar tab de produtos
        logger.info("Carregando módulo Gestão de Produtos")
        tab_produtos = ProdutoView(notebook)
        notebook.add(tab_produtos, text="Gestão de Produtos")
        
        # Menu principal
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Exportar Dados", 
                             command=lambda: messagebox.showinfo("Info", "Funcionalidade em desenvolvimento"))
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        
        # Menu Ajuda
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Documentação", 
                             command=lambda: messagebox.showinfo("Info", "Consulte o arquivo README.md"))
        help_menu.add_command(label="Sobre", command=lambda: messagebox.showinfo(
            "Sobre", "StoreAnalyzer v1.0\n\nAnálise de dados e gestão de produtos para lojas de suplementos"))
        
        # Configurar comportamento de fechamento
        root.protocol("WM_DELETE_WINDOW", lambda: confirmar_saida(root))
        
        logger.info("Aplicação inicializada com sucesso")
        root.mainloop()
    
    except Exception as e:
        logger.error(f"Erro ao inicializar aplicação: {str(e)}", exc_info=True)
        messagebox.showerror("Erro", f"Erro ao inicializar aplicação: {str(e)}")

def confirmar_saida(root):
    """Confirma a saída da aplicação"""
    if messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?"):
        logger.info("Aplicação encerrada pelo usuário")
        root.destroy()

if __name__ == "__main__":
    # Configurar logging
    logger = configurar_logging()
    
    # Configurar handler global de exceções
    sys.excepthook = handler_excecao
    
    # Iniciar aplicação
    iniciar_app()