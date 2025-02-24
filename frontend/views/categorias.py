import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, Optional, Dict

if TYPE_CHECKING:
    from main import MainApplication

class CategoriaDialog:
    def __init__(self, parent, controller, categoria: Optional[Dict] = None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nova Categoria" if not categoria else "Editar Categoria")
        self.dialog.geometry("400x250")
        self.controller = controller
        self.categoria = categoria
        self.resultado = None
        
        # Centraliza o diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.criar_widgets()
        
        if categoria:
            self.preencher_dados(categoria)
    
    def criar_widgets(self):
        # Nome
        ttk.Label(self.dialog, text="Nome:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.nome_entry = ttk.Entry(self.dialog, width=30)
        self.nome_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Categoria Pai (opcional)
        ttk.Label(self.dialog, text="Categoria Pai:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.categoria_pai_combobox = ttk.Combobox(self.dialog, state="readonly")
        self.categoria_pai_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.carregar_categorias()
        
        # Botões
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side="left", padx=5)
    
    def carregar_categorias(self):
        try:
            categorias = self.controller.api_client.listar_categorias()
            self.categoria_pai_combobox['values'] = ["Nenhuma"] + [c['nome'] for c in categorias]
            self.categoria_pai_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar categorias: {str(e)}")
    
    def preencher_dados(self, categoria: Dict):
        self.nome_entry.insert(0, categoria['nome'])
        if categoria.get('categoria_pai_id'):
            categorias = self.controller.api_client.listar_categorias()
            for i, cat in enumerate(categorias, 1):  # começa em 1 por causa do "Nenhuma"
                if cat['id'] == categoria['categoria_pai_id']:
                    self.categoria_pai_combobox.current(i)
                    break
    
    def salvar(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome da categoria é obrigatório")
            return
        
        categoria_pai = self.categoria_pai_combobox.get()
        dados = {
            'nome': nome,
            'categoria_pai_id': None
        }
        
        if categoria_pai != "Nenhuma":
            categorias = self.controller.api_client.listar_categorias()
            for cat in categorias:
                if cat['nome'] == categoria_pai:
                    dados['categoria_pai_id'] = cat['id']
                    break
        
        self.resultado = dados
        self.dialog.destroy()
    
    def cancelar(self):
        self.dialog.destroy()

class CategoriasView(ttk.Frame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Frame superior com botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Nova Categoria", command=self.nova_categoria).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_categoria).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_categoria).pack(side="left", padx=5)
        
        # Treeview para listar categorias
        self.tree = ttk.Treeview(self, columns=("nome", "categoria_pai"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar colunas
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria_pai", text="Categoria Pai")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def nova_categoria(self):
        dialog = CategoriaDialog(self, self.controller)
        self.wait_window(dialog.dialog)
        if dialog.resultado:
            try:
                self.controller.api_client.criar_categoria(dialog.resultado)
                self.atualizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar categoria: {str(e)}")
    
    def editar_categoria(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria para editar")
            return
        
        item_id = selection[0]
        categoria_id = self.tree.item(item_id)['values'][0]
        
        try:
            categoria = self.controller.api_client.obter_categoria(categoria_id)
            dialog = CategoriaDialog(self, self.controller, categoria)
            self.wait_window(dialog.dialog)
            
            if dialog.resultado:
                self.controller.api_client.atualizar_categoria(categoria_id, dialog.resultado)
                self.atualizar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar categoria: {str(e)}")
    
    def excluir_categoria(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta categoria?\n"
                              "Todas as subcategorias também serão excluídas."):
            item_id = selection[0]
            categoria_id = self.tree.item(item_id)['values'][0]
            
            try:
                self.controller.api_client.deletar_categoria(categoria_id)
                self.atualizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir categoria: {str(e)}")
    
    def atualizar(self):
        """Atualiza a lista de categorias"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            categorias = self.controller.api_client.listar_categorias()
            
            # Criar dicionário de categorias para facilitar a busca
            categorias_dict = {c['id']: c for c in categorias}
            
            for categoria in categorias:
                categoria_pai_nome = ""
                if categoria.get('categoria_pai_id'):
                    categoria_pai = categorias_dict.get(categoria['categoria_pai_id'])
                    if categoria_pai:
                        categoria_pai_nome = categoria_pai['nome']
                
                self.tree.insert("", "end", values=(
                    categoria['nome'],
                    categoria_pai_nome
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar categorias: {str(e)}") 