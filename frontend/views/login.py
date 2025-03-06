import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainApplication

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Título
        titulo = ctk.CTkLabel(self, text="Login", font=("Helvetica", 16, "bold"))
        titulo.pack(pady=20)
        
        # Email
        ctk.CTkLabel(self, text="Email:").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, width=300)
        self.email_entry.pack(pady=5)
        
        # Senha
        ctk.CTkLabel(self, text="Senha:").pack(pady=5)
        self.senha_entry = ctk.CTkEntry(self, width=300, show="*")
        self.senha_entry.pack(pady=5)
        
        # Botões
        btn_container = ctk.CTkFrame(self)
        btn_container.pack(pady=20)
        
        ctk.CTkButton(btn_container, text="Entrar", command=self.login).pack(side="left", padx=5)
        ctk.CTkButton(btn_container, text="Registrar", command=self.mostrar_registro).pack(side="left", padx=5)
        
        # Frame de registro (inicialmente oculto)
        self.registro_frame = ctk.CTkFrame(self)
        
        # Campos do registro
        ctk.CTkLabel(self.registro_frame, text="Nome:").pack(pady=5)
        self.nome_entry = ctk.CTkEntry(self.registro_frame, width=300)
        self.nome_entry.pack(pady=5)
        
        ctk.CTkLabel(self.registro_frame, text="Email:").pack(pady=5)
        self.reg_email_entry = ctk.CTkEntry(self.registro_frame, width=300)
        self.reg_email_entry.pack(pady=5)
        
        ctk.CTkLabel(self.registro_frame, text="Senha:").pack(pady=5)
        self.reg_senha_entry = ctk.CTkEntry(self.registro_frame, width=300, show="*")
        self.reg_senha_entry.pack(pady=5)
        
        btn_reg_container = ctk.CTkFrame(self.registro_frame)
        btn_reg_container.pack(pady=20)
        
        ctk.CTkButton(btn_reg_container, text="Confirmar", command=self.registrar).pack(side="left", padx=5)
        ctk.CTkButton(btn_reg_container, text="Voltar", command=self.mostrar_login).pack(side="left", padx=5)
    
    def login(self):
        """Realiza o login do usuário"""
        try:
            resposta = self.controller.api_client.login(
                self.email_entry.get(),
                self.senha_entry.get()
            )
            self.controller.iniciar_aplicacao(resposta['token'])
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def registrar(self):
        """Registra um novo usuário"""
        try:
            self.controller.api_client.registrar(
                self.nome_entry.get(),
                self.reg_email_entry.get(),
                self.reg_senha_entry.get()
            )
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def mostrar_registro(self):
        """Mostra o formulário de registro"""
        self.registro_frame.pack(pady=20)
    
    def mostrar_login(self):
        """Volta para o formulário de login"""
        self.registro_frame.pack_forget()
        self.limpar_campos()
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.email_entry.delete(0, 'end')
        self.senha_entry.delete(0, 'end')
        self.nome_entry.delete(0, 'end')
        self.reg_email_entry.delete(0, 'end')
        self.reg_senha_entry.delete(0, 'end') 