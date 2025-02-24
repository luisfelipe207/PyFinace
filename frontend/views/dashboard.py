import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from main import MainApplication

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Container superior para resumo financeiro
        resumo_frame = ttk.LabelFrame(self, text="Resumo Financeiro")
        resumo_frame.pack(fill="x", padx=10, pady=5)
        
        # Saldo, Receitas e Despesas
        self.saldo_label = ttk.Label(resumo_frame, text="Saldo: R$ 0,00", font=("Helvetica", 12, "bold"))
        self.saldo_label.pack(side="left", padx=20, pady=10)
        
        self.receitas_label = ttk.Label(resumo_frame, text="Receitas: R$ 0,00", font=("Helvetica", 12))
        self.receitas_label.pack(side="left", padx=20, pady=10)
        
        self.despesas_label = ttk.Label(resumo_frame, text="Despesas: R$ 0,00", font=("Helvetica", 12))
        self.despesas_label.pack(side="left", padx=20, pady=10)
        
        # Container para gráficos
        graficos_frame = ttk.Frame(self)
        graficos_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para o gráfico de fluxo
        self.fluxo_frame = ttk.LabelFrame(graficos_frame, text="Fluxo de Caixa")
        self.fluxo_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Frame para o gráfico de categorias
        self.categorias_frame = ttk.LabelFrame(graficos_frame, text="Distribuição por Categorias")
        self.categorias_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Criar gráficos iniciais
        self.criar_graficos()
    
    def criar_graficos(self):
        """Cria os gráficos vazios"""
        # Gráfico de Fluxo de Caixa
        self.fig_fluxo = plt.Figure(figsize=(6, 4))
        self.canvas_fluxo = FigureCanvasTkAgg(self.fig_fluxo, self.fluxo_frame)
        self.canvas_fluxo.get_tk_widget().pack(fill="both", expand=True)
        
        # Gráfico de Categorias
        self.fig_categorias = plt.Figure(figsize=(6, 4))
        self.canvas_categorias = FigureCanvasTkAgg(self.fig_categorias, self.categorias_frame)
        self.canvas_categorias.get_tk_widget().pack(fill="both", expand=True)
    
    def atualizar(self):
        """Atualiza os dados do dashboard"""
        try:
            # Obtém dados do último mês
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=30)
            
            # Obtém relatório de fluxo
            fluxo = self.controller.api_client.obter_relatorio_fluxo({
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
            })
            
            # Atualiza labels
            self.saldo_label.config(text=f"Saldo: R$ {fluxo['saldo']:.2f}")
            self.receitas_label.config(text=f"Receitas: R$ {fluxo['receitas']:.2f}")
            self.despesas_label.config(text=f"Despesas: R$ {fluxo['despesas']:.2f}")
            
            # Atualiza gráfico de fluxo
            self.atualizar_grafico_fluxo(fluxo['transacoes'])
            
            # Obtém e atualiza gráfico de categorias
            categorias = self.controller.api_client.obter_relatorio_categorias({
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
            })
            self.atualizar_grafico_categorias(categorias)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")
    
    def atualizar_grafico_fluxo(self, transacoes):
        """Atualiza o gráfico de fluxo de caixa"""
        self.fig_fluxo.clear()
        ax = self.fig_fluxo.add_subplot(111)
        
        # Organiza transações por data
        datas = []
        valores = []
        saldo_acumulado = 0
        
        for t in sorted(transacoes, key=lambda x: x['data']):
            datas.append(datetime.strptime(t['data'], '%Y-%m-%d'))
            if t['tipo'] == 'receita':
                saldo_acumulado += t['valor']
            else:
                saldo_acumulado -= t['valor']
            valores.append(saldo_acumulado)
        
        ax.plot(datas, valores)
        ax.set_title('Evolução do Saldo')
        ax.set_xlabel('Data')
        ax.set_ylabel('Saldo (R$)')
        self.fig_fluxo.autofmt_xdate()
        self.canvas_fluxo.draw()
    
    def atualizar_grafico_categorias(self, dados_categorias):
        """Atualiza o gráfico de distribuição por categorias"""
        self.fig_categorias.clear()
        ax = self.fig_categorias.add_subplot(111)
        
        categorias = [d['categoria'] for d in dados_categorias]
        despesas = [d['total_despesas'] for d in dados_categorias]
        
        ax.pie(despesas, labels=categorias, autopct='%1.1f%%')
        ax.set_title('Distribuição de Despesas por Categoria')
        self.canvas_categorias.draw() 