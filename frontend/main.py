import tkinter as tk
from tkinter import ttk
from views.dashboard import DashboardView
from views.transacoes import TransacoesView
from views.categorias import CategoriasView
from views.relatorios import RelatoriosView
from views.login import LoginView
from utils.api_client import APIClient

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Controle Financeiro")
        self.geometry("1024x768")
        
        # Configuração do cliente API
        self.api_client = APIClient("http://localhost:5000/api")
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Container principal
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dicionário para armazenar as frames
        self.frames = {}
        
        # Inicialmente, mostrar tela de login
        self.mostrar_login()
    
    def mostrar_login(self):
        """Mostra a tela de login"""
        self.limpar_frames()
        login_frame = LoginView(self.container, self)
        login_frame.grid(row=0, column=0, sticky="nsew")
        self.frames['login'] = login_frame
    
    def iniciar_aplicacao(self, token):
        """Inicia a aplicação principal após o login"""
        self.api_client.set_token(token)
        self.limpar_frames()
        self.criar_menu()
        self.mostrar_dashboard()
    
    def criar_menu(self):
        """Cria o menu principal da aplicação"""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # Menu Principal
        menu_principal = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Principal", menu=menu_principal)
        menu_principal.add_command(label="Dashboard", command=self.mostrar_dashboard)
        menu_principal.add_command(label="Transações", command=self.mostrar_transacoes)
        menu_principal.add_command(label="Categorias", command=self.mostrar_categorias)
        menu_principal.add_command(label="Relatórios", command=self.mostrar_relatorios)
        menu_principal.add_separator()
        menu_principal.add_command(label="Sair", command=self.logout)
    
    def mostrar_frame(self, frame_class):
        """Mostra uma frame específica"""
        if frame_class.__name__ not in self.frames:
            frame = frame_class(self.container, self)
            self.frames[frame_class.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        frame = self.frames[frame_class.__name__]
        frame.tkraise()
        frame.atualizar()  # Atualiza os dados da frame
    
    def mostrar_dashboard(self):
        """Mostra a tela de dashboard"""
        self.mostrar_frame(DashboardView)
    
    def mostrar_transacoes(self):
        """Mostra a tela de transações"""
        self.mostrar_frame(TransacoesView)
    
    def mostrar_categorias(self):
        """Mostra a tela de categorias"""
        self.mostrar_frame(CategoriasView)
    
    def mostrar_relatorios(self):
        """Mostra a tela de relatórios"""
        self.mostrar_frame(RelatoriosView)
    
    def limpar_frames(self):
        """Remove todas as frames existentes"""
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
    
    def logout(self):
        """Realiza o logout do usuário"""
        self.api_client.clear_token()
        self.mostrar_login()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop() 