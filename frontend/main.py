import customtkinter as ctk
from views.dashboard import DashboardView
from views.transacoes import TransacoesView
from views.categorias import CategoriasView
from views.relatorios import RelatoriosView
from views.login import LoginView
from utils.api_client import APIClient

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Controle Financeiro")
        self.geometry("1024x768")
        
        # Configuração do cliente API
        self.api_client = APIClient("http://localhost:5000/api")
        
        # Configuração do estilo
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("blue")  # Tema azul
        
        # Container principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        # Menu
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(side="top", fill="x")
        
        # Botões do menu
        ctk.CTkButton(self.menu_frame, text="Dashboard", command=self.mostrar_dashboard).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self.menu_frame, text="Transações", command=self.mostrar_transacoes).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self.menu_frame, text="Categorias", command=self.mostrar_categorias).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self.menu_frame, text="Relatórios", command=self.mostrar_relatorios).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self.menu_frame, text="Sair", command=self.logout).pack(side="right", padx=5, pady=5)
        
        # Dicionário para armazenar as frames
        self.frames = {}
        
        # Inicialmente, mostrar tela de login
        self.mostrar_login()
    
    def mostrar_login(self):
        """Mostra a tela de login"""
        self.limpar_frames()
        login_frame = LoginView(self.container, self)
        login_frame.pack(expand=True)  # Centraliza o frame
        self.frames['login'] = login_frame
    
    def iniciar_aplicacao(self, token):
        """Inicia a aplicação principal após o login"""
        self.api_client.set_token(token)
        self.limpar_frames()
        self.mostrar_dashboard()
    
    def mostrar_frame(self, frame_class):
        """Mostra uma frame específica"""
        if frame_class.__name__ not in self.frames:
            frame = frame_class(self.container, self)
            self.frames[frame_class.__name__] = frame
            frame.pack(expand=True)  # Centraliza o frame
        
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