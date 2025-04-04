import tkinter as tk
from tkinter import ttk, messagebox
from controllers.produto_controller import ProdutoController

class ProdutoView(ttk.Frame):
    """Interface gráfica para gestão de produtos"""
    
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.controller = ProdutoController()
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal dividido em duas partes
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo: lista de produtos
        frame_lista = tk.LabelFrame(frame, text="Lista de Produtos", padx=10, pady=10)
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Barra de ferramentas para operações de produtos
        frame_tools = tk.Frame(frame_lista)
        frame_tools.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(frame_tools, text="Novo Produto", command=self.abrir_form_novo_produto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Editar", command=self.editar_produto_selecionado).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Remover", command=self.remover_produto_selecionado).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_tools, text="Atualizar", command=self.atualizar_lista_produtos).pack(side=tk.LEFT, padx=5)
        
        # TreeView para mostrar os produtos
        colunas = ("ID", "Nome", "Categoria", "Preço", "Stock")
        self.tree_produtos = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        
        # Configurar cabeçalhos e colunas
        for col in colunas:
            self.tree_produtos.heading(col, text=col)
            width = 70 if col in ("ID", "Preço", "Stock") else 150
            self.tree_produtos.column(col, width=width)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_produtos.pack(fill=tk.BOTH, expand=True)
        
        # Evento de clique duplo para editar produto
        self.tree_produtos.bind("<Double-1>", lambda event: self.editar_produto_selecionado())
        
        # Painel direito: detalhes do produto
        self.frame_detalhes = tk.LabelFrame(frame, text="Detalhes do Produto", padx=10, pady=10)
        self.frame_detalhes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Campos do formulário
        campos = [
            ("ID:", "entry_id", True),  # (label, nome_campo, somente_leitura)
            ("Nome:", "entry_nome", False),
            ("Categoria:", "combo_categoria", False),
            ("Preço Base:", "entry_preco", False),
            ("Stock:", "entry_stock", False),
            ("Descrição:", "text_descricao", False)
        ]
        
        # Criar campos de formulário
        for i, (label_text, campo_nome, somente_leitura) in enumerate(campos):
            frame_campo = tk.Frame(self.frame_detalhes)
            frame_campo.pack(fill=tk.X, pady=5)
            
            tk.Label(frame_campo, text=label_text, width=10, anchor="w").pack(side=tk.LEFT)
            
            if campo_nome == "combo_categoria":
                categorias = self.controller.obter_categorias() or ["Ganhos Musculares", "Energia", "Recuperação", "Saúde"]
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
        
        # Botões de ação
        frame_botoes = tk.Frame(self.frame_detalhes)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        tk.Button(frame_botoes, text="Guardar", command=self.guardar_produto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        # Carregar lista de produtos
        self.atualizar_lista_produtos()
        
        # Inicialmente, limpar o formulário
        self.limpar_formulario()
    
    def atualizar_lista_produtos(self):
        """Atualiza a lista de produtos na TreeView"""
        # Limpar a TreeView
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        # Obter todos os produtos
        produtos = self.controller.listar_todos()
        
        if produtos:
            # Preencher a TreeView com os dados dos produtos
            for produto in produtos:
                self.tree_produtos.insert("", tk.END, values=(
                    produto.id,
                    produto.nome,
                    produto.categoria,
                    f"{produto.preco_base:.2f} €",
                    produto.stock
                ))
    
    def limpar_formulario(self):
        """Limpa o formulário de produto"""
        # Limpar os campos
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        
        self.entry_nome.delete(0, tk.END)
        
        # Reconfigurar o combobox
        categorias = self.controller.obter_categorias() or ["Ganhos Musculares", "Energia", "Recuperação", "Saúde"]
        self.combo_categoria.config(values=categorias)
        self.combo_categoria.delete(0, tk.END)
        
        self.entry_preco.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        
        # Atualizar o título do frame
        self.frame_detalhes.config(text="Detalhes do Produto")
    
    def abrir_form_novo_produto(self):
        """Abre o formulário para criar um novo produto"""
        self.limpar_formulario()
        self.frame_detalhes.config(text="Novo Produto")
    
    def editar_produto_selecionado(self):
        """Abre o formulário para editar o produto selecionado"""
        # Obter a seleção atual
        selection = self.tree_produtos.selection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")
            return
        
        # Obter o ID do produto selecionado
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        
        # Obter os detalhes do produto
        produto = self.controller.obter_produto(produto_id)
        
        if not produto:
            messagebox.showerror("Erro", "Não foi possível obter os detalhes do produto")
            return
        
        # Preencher o formulário com os detalhes do produto
        self.limpar_formulario()
        
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, produto.id)
        self.entry_id.config(state="readonly")
        
        self.entry_nome.insert(0, produto.nome)
        self.combo_categoria.set(produto.categoria)
        self.entry_preco.insert(0, produto.preco_base)
        self.entry_stock.insert(0, produto.stock)
        self.text_descricao.insert("1.0", produto.descricao)
        
        self.frame_detalhes.config(text=f"Editar Produto: {produto.nome}")
    
    def remover_produto_selecionado(self):
        """Remove o produto selecionado"""
        # Obter a seleção atual
        selection = self.tree_produtos.selection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para remover")
            return
        
        # Obter o ID do produto selecionado
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        produto_nome = item['values'][1]
        
        # Confirmar a remoção
        confirmar = messagebox.askyesno("Confirmar", f"Deseja realmente remover o produto '{produto_nome}'?")
        
        if confirmar:
            # Remover o produto
            sucesso, mensagem = self.controller.remover_produto(produto_id)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Produto '{produto_nome}' removido com sucesso")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
            else:
                messagebox.showerror("Erro", mensagem)
    
    def guardar_produto(self):
        """Guarda um produto (novo ou atualizado)"""
        # Obter os valores do formulário
        produto_id = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get().strip()
        preco_base = self.entry_preco.get().strip()
        stock = self.entry_stock.get().strip()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        if produto_id:
            # Atualizar produto existente
            sucesso, mensagem = self.controller.atualizar_produto(
                int(produto_id), nome, categoria, preco_base, stock, descricao)
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
            else:
                messagebox.showwarning("Aviso", mensagem)
        else:
            # Adicionar novo produto
            sucesso, resultado = self.controller.adicionar_produto(
                nome, categoria, preco_base, stock, descricao)
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso (ID: {resultado})")
                self.atualizar_lista_produtos()
                self.limpar_formulario()
            else:
                messagebox.showwarning("Aviso", resultado)