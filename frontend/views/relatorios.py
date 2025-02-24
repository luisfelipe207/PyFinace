import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import pandas as pd
from tkinter import filedialog

if TYPE_CHECKING:
    from main import MainApplication

class RelatoriosView(ttk.Frame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(self, text="Período")
        filtros_frame.pack(fill="x", padx=10, pady=5)
        
        # Data inicial
        ttk.Label(filtros_frame, text="De:").pack(side="left", padx=5)
        self.data_inicio = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_inicio.pack(side="left", padx=5)
        
        # Data final
        ttk.Label(filtros_frame, text="Até:").pack(side="left", padx=5)
        self.data_fim = DateEntry(filtros_frame, width=12, locale='pt_BR')
        self.data_fim.pack(side="left", padx=5)
        
        # Botão de atualizar
        ttk.Button(filtros_frame, text="Atualizar", command=self.atualizar).pack(side="left", padx=5)
        ttk.Button(filtros_frame, text="Exportar CSV", command=self.exportar_csv).pack(side="right", padx=5)
        
        # Container para gráficos
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Aba de Fluxo de Caixa
        self.fluxo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fluxo_frame, text="Fluxo de Caixa")
        
        # Aba de Categorias
        self.categorias_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.categorias_frame, text="Categorias")
        
        # Aba de Resumo
        self.resumo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resumo_frame, text="Resumo")
        
        # Criar gráficos
        self.criar_graficos()
        
        # Criar área de resumo
        self.criar_resumo()
    
    def criar_graficos(self):
        """Cria os gráficos vazios"""
        # Gráfico de Fluxo de Caixa
        self.fig_fluxo = plt.Figure(figsize=(10, 6))
        self.canvas_fluxo = FigureCanvasTkAgg(self.fig_fluxo, self.fluxo_frame)
        self.canvas_fluxo.get_tk_widget().pack(fill="both", expand=True)
        
        # Gráfico de Categorias
        self.fig_categorias = plt.Figure(figsize=(10, 6))
        self.canvas_categorias = FigureCanvasTkAgg(self.fig_categorias, self.categorias_frame)
        self.canvas_categorias.get_tk_widget().pack(fill="both", expand=True)
    
    def criar_resumo(self):
        """Cria a área de resumo financeiro"""
        # Frame para valores
        valores_frame = ttk.Frame(self.resumo_frame)
        valores_frame.pack(fill="x", padx=10, pady=5)
        
        # Labels para valores
        self.receitas_label = ttk.Label(valores_frame, text="Receitas Totais: R$ 0,00", font=("Helvetica", 12))
        self.receitas_label.pack(pady=5)
        
        self.despesas_label = ttk.Label(valores_frame, text="Despesas Totais: R$ 0,00", font=("Helvetica", 12))
        self.despesas_label.pack(pady=5)
        
        self.saldo_label = ttk.Label(valores_frame, text="Saldo: R$ 0,00", font=("Helvetica", 12, "bold"))
        self.saldo_label.pack(pady=5)
        
        # Treeview para detalhes por categoria
        self.tree = ttk.Treeview(self.resumo_frame, columns=("categoria", "receitas", "despesas", "saldo"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar colunas
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("receitas", text="Receitas")
        self.tree.heading("despesas", text="Despesas")
        self.tree.heading("saldo", text="Saldo")
    
    def atualizar(self):
        """Atualiza todos os relatórios"""
        try:
            filtros = {
                'data_inicio': self.data_inicio.get_date().strftime('%Y-%m-%d'),
                'data_fim': self.data_fim.get_date().strftime('%Y-%m-%d')
            }
            
            # Atualizar relatório de fluxo
            fluxo = self.controller.api_client.obter_relatorio_fluxo(filtros)
            self.atualizar_grafico_fluxo(fluxo['transacoes'])
            
            # Atualizar relatório de categorias
            categorias = self.controller.api_client.obter_relatorio_categorias(filtros)
            self.atualizar_grafico_categorias(categorias)
            
            # Atualizar resumo
            self.atualizar_resumo(fluxo, categorias)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar relatórios: {str(e)}")
    
    def atualizar_grafico_fluxo(self, transacoes):
        """Atualiza o gráfico de fluxo de caixa"""
        self.fig_fluxo.clear()
        ax = self.fig_fluxo.add_subplot(111)
        
        # Organizar transações por data
        df = pd.DataFrame(transacoes)
        df['data'] = pd.to_datetime(df['data'])
        df['valor'] = df.apply(lambda x: x['valor'] if x['tipo'] == 'receita' else -x['valor'], axis=1)
        
        # Calcular saldo acumulado
        df = df.sort_values('data')
        df['saldo_acumulado'] = df['valor'].cumsum()
        
        # Plotar gráfico
        ax.plot(df['data'], df['saldo_acumulado'], label='Saldo')
        ax.bar(df['data'], df['valor'], alpha=0.3, 
               color=df['valor'].apply(lambda x: 'green' if x > 0 else 'red'))
        
        ax.set_title('Fluxo de Caixa')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor (R$)')
        ax.legend()
        self.fig_fluxo.autofmt_xdate()
        self.canvas_fluxo.draw()
    
    def atualizar_grafico_categorias(self, categorias):
        """Atualiza o gráfico de distribuição por categorias"""
        self.fig_categorias.clear()
        
        # Criar dois subplots: um para receitas e outro para despesas
        ax1 = self.fig_categorias.add_subplot(121)
        ax2 = self.fig_categorias.add_subplot(122)
        
        # Preparar dados
        nomes = [c['categoria'] for c in categorias]
        receitas = [c['total_receitas'] for c in categorias]
        despesas = [c['total_despesas'] for c in categorias]
        
        # Plotar gráficos de pizza
        if sum(receitas) > 0:
            ax1.pie(receitas, labels=nomes, autopct='%1.1f%%')
            ax1.set_title('Receitas por Categoria')
        
        if sum(despesas) > 0:
            ax2.pie(despesas, labels=nomes, autopct='%1.1f%%')
            ax2.set_title('Despesas por Categoria')
        
        self.canvas_categorias.draw()
    
    def atualizar_resumo(self, fluxo, categorias):
        """Atualiza o resumo financeiro"""
        # Atualizar labels
        self.receitas_label.config(text=f"Receitas Totais: R$ {fluxo['receitas']:.2f}")
        self.despesas_label.config(text=f"Despesas Totais: R$ {fluxo['despesas']:.2f}")
        self.saldo_label.config(text=f"Saldo: R$ {fluxo['saldo']:.2f}")
        
        # Atualizar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cat in categorias:
            saldo = cat['total_receitas'] - cat['total_despesas']
            self.tree.insert("", "end", values=(
                cat['categoria'],
                f"R$ {cat['total_receitas']:.2f}",
                f"R$ {cat['total_despesas']:.2f}",
                f"R$ {saldo:.2f}"
            ))
    
    def exportar_csv(self):
        """Exporta os dados do período para CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Exportar Relatório"
            )
            
            if not filename:
                return
            
            filtros = {
                'data_inicio': self.data_inicio.get_date().strftime('%Y-%m-%d'),
                'data_fim': self.data_fim.get_date().strftime('%Y-%m-%d')
            }
            
            # Obter dados
            transacoes = self.controller.api_client.listar_transacoes(filtros)
            
            # Criar DataFrame
            df = pd.DataFrame(transacoes)
            
            # Salvar CSV
            df.to_csv(filename, index=False)
            messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}") 