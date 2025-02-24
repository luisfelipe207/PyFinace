import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, Optional, Dict
from datetime import datetime
from tkcalendar import DateEntry

if TYPE_CHECKING:
    from main import MainApplication

class TransacaoDialog:
    def __init__(self, parent, controller, transacao: Optional[Dict] = None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nova Transação" if not transacao else "Editar Transação")
        self.dialog.geometry("400x350")
        self.controller = controller
        self.transacao = transacao
        self.resultado = None
        
        # Centraliza o diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.criar_widgets()
        
        if transacao:
            self.preencher_dados(transacao)
    
    def criar_widgets(self):
        # Tipo de Transação
        ttk.Label(self.dialog, text="Tipo:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.tipo_var = tk.StringVar(value="receita")
        ttk.Radiobutton(self.dialog, text="Receita", variable=self.tipo_var, value="receita").grid(row=0, column=1, pady=5, sticky="w")
        ttk.Radiobutton(self.dialog, text="Despesa", variable=self.tipo_var, value="despesa").grid(row=0, column=2, pady=5, sticky="w")
        
        # Valor
        ttk.Label(self.dialog, text="Valor (R$):").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.valor_entry = ttk.Entry(self.dialog)
        self.valor_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        
        # Data
        ttk.Label(self.dialog, text="Data:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.data_entry = DateEntry(self.dialog, width=20, locale='pt_BR')
        self.data_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        
        # Categoria
        ttk.Label(self.dialog, text="Categoria:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.categoria_combobox = ttk.Combobox(self.dialog, state="readonly")
        self.categoria_combobox.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        self.carregar_categorias()
        
        # Descrição
        ttk.Label(self.dialog, text="Descrição:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.descricao_text = tk.Text(self.dialog, height=4, width=30)
        self.descricao_text.grid(row=4, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        
        # Botões
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side="left", padx=5)
    
    def carregar_categorias(self):
        try:
            categorias = self.controller.api_client.listar_categorias()
            self.categoria_combobox['values'] = [c['nome'] for c in categorias]
            if self.categoria_combobox['values']:
                self.categoria_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar categorias: {str(e)}")
    
    def preencher_dados(self, transacao: Dict):
        self.tipo_var.set(transacao['tipo'])
        self.valor_entry.insert(0, str(transacao['valor']))
        self.data_entry.set_date(datetime.strptime(transacao['data_transacao'], '%Y-%m-%d'))
        if transacao.get('descricao'):
            self.descricao_text.insert('1.0', transacao['descricao'])
        if transacao.get('categoria_id'):
            # Encontrar índice da categoria
            categorias = self.controller.api_client.listar_categorias()
            for i, cat in enumerate(categorias):
                if cat['id'] == transacao['categoria_id']:
                    self.categoria_combobox.current(i)
                    break
    
    def salvar(self):
        try:
            valor = float(self.valor_entry.get().replace(',', '.'))
            data = self.data_entry.get_date().strftime('%Y-%m-%d')
            categoria_nome = self.categoria_combobox.get()
            
            # Obter ID da categoria
            categorias = self.controller.api_client.listar_categorias()
            categoria_id = next(c['id'] for c in categorias if c['nome'] == categoria_nome)
            
            dados = {
                'valor': valor,
                'tipo': self.tipo_var.get(),
                'data_transacao': data,
                'categoria_id': categoria_id,
                'descricao': self.descricao_text.get('1.0', 'end-1c')
            }
            
            self.resultado = dados
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")
    
    def cancelar(self):
        self.dialog.destroy()

class TransacoesView(ttk.Frame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Frame superior com botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Nova Transação", command=self.nova_transacao).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_transacao).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_transacao).pack(side="left", padx=5)
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(self, text="Filtros")
        filtros_frame.pack(fill="x", padx=10, pady=5)
        
        # Data inicial
        ttk.Label(filtros_frame, text="De:").pack(side="left", padx=5)
        self.data_inicio = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_inicio.pack(side="left", padx=5)
        
        # Data final
        ttk.Label(filtros_frame, text="Até:").pack(side="left", padx=5)
        self.data_fim = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_fim.pack(side="left", padx=5)
        
        # Tipo
        ttk.Label(filtros_frame, text="Tipo:").pack(side="left", padx=5)
        self.tipo_filtro = ttk.Combobox(filtros_frame, values=["Todos", "Receita", "Despesa"], state="readonly", width=10)
        self.tipo_filtro.set("Todos")
        self.tipo_filtro.pack(side="left", padx=5)
        
        ttk.Button(filtros_frame, text="Filtrar", command=self.atualizar).pack(side="left", padx=5)
        
        # Treeview para listar transações
        self.tree = ttk.Treeview(self, columns=("data", "tipo", "valor", "categoria", "descricao"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar colunas
        self.tree.heading("data", text="Data")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("descricao", text="Descrição")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def nova_transacao(self):
        dialog = TransacaoDialog(self, self.controller)
        self.wait_window(dialog.dialog)
        if dialog.resultado:
            try:
                self.controller.api_client.criar_transacao(dialog.resultado)
                self.atualizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar transação: {str(e)}")
    
    def editar_transacao(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma transação para editar")
            return
        
        item_id = selection[0]
        transacao_id = self.tree.item(item_id)['values'][0]
        
        try:
            transacao = self.controller.api_client.obter_transacao(transacao_id)
            dialog = TransacaoDialog(self, self.controller, transacao)
            self.wait_window(dialog.dialog)
            
            if dialog.resultado:
                self.controller.api_client.atualizar_transacao(transacao_id, dialog.resultado)
                self.atualizar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar transação: {str(e)}")
    
    def excluir_transacao(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma transação para excluir")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta transação?"):
            item_id = selection[0]
            transacao_id = self.tree.item(item_id)['values'][0]
            
            try:
                self.controller.api_client.deletar_transacao(transacao_id)
                self.atualizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir transação: {str(e)}")
    
    def atualizar(self):
        """Atualiza a lista de transações"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            filtros = {
                'data_inicio': self.data_inicio.get_date().strftime('%Y-%m-%d'),
                'data_fim': self.data_fim.get_date().strftime('%Y-%m-%d')
            }
            
            if self.tipo_filtro.get() != "Todos":
                filtros['tipo'] = self.tipo_filtro.get().lower()
            
            transacoes = self.controller.api_client.listar_transacoes(filtros)
            
            for t in transacoes:
                self.tree.insert("", "end", values=(
                    t['data_transacao'],
                    t['tipo'].capitalize(),
                    f"R$ {t['valor']:.2f}",
                    t.get('categoria', {}).get('nome', ''),
                    t.get('descricao', '')
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar transações: {str(e)}") 