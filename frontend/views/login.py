import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MainApplication

class LoginView(ttk.Frame):
    def __init__(self, parent, controller: 'MainApplication'):
        super().__init__(parent)
        self.controller = controller
        
        # Container central
        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.4, anchor="center")
        
        # Título
        titulo = ttk.Label(container, text="Login", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Email
        ttk.Label(container, text="Email:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.email_entry = ttk.Entry(container, width=30)
        self.email_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Senha
        ttk.Label(container, text="Senha:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.senha_entry = ttk.Entry(container, width=30, show="*")
        self.senha_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Botões
        btn_container = ttk.Frame(container)
        btn_container.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_container, text="Entrar", command=self.login).pack(side="left", padx=5)
        ttk.Button(btn_container, text="Registrar", command=self.mostrar_registro).pack(side="left", padx=5)
        
        # Frame de registro (inicialmente oculto)
        self.registro_frame = ttk.Frame(self)
        
        # Campos do registro
        ttk.Label(self.registro_frame, text="Nome:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.nome_entry = ttk.Entry(self.registro_frame, width=30)
        self.nome_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(self.registro_frame, text="Email:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.reg_email_entry = ttk.Entry(self.registro_frame, width=30)
        self.reg_email_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(self.registro_frame, text="Senha:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.reg_senha_entry = ttk.Entry(self.registro_frame, width=30, show="*")
        self.reg_senha_entry.grid(row=2, column=1, pady=5, padx=5)
        
        btn_reg_container = ttk.Frame(self.registro_frame)
        btn_reg_container.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_reg_container, text="Confirmar", command=self.registrar).pack(side="left", padx=5)
        ttk.Button(btn_reg_container, text="Voltar", command=self.mostrar_login).pack(side="left", padx=5)
    
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
        self.registro_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    def mostrar_login(self):
        """Volta para o formulário de login"""
        self.registro_frame.place_forget()
        self.limpar_campos()
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.email_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.reg_email_entry.delete(0, tk.END)
        self.reg_senha_entry.delete(0, tk.END) 