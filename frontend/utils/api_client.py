import requests
from typing import Optional, Dict, Any
import json

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
    
    def set_token(self, token: str):
        """Define o token de autenticação"""
        self.token = token
    
    def clear_token(self):
        """Remove o token de autenticação"""
        self.token = None
    
    def get_headers(self) -> Dict[str, str]:
        """Retorna os headers para as requisições"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def login(self, email: str, senha: str) -> Dict[str, Any]:
        """Realiza o login do usuário"""
        response = requests.post(
            f'{self.base_url}/auth/login',
            json={'email': email, 'senha': senha}
        )
        response.raise_for_status()
        return response.json()
    
    def registrar(self, nome: str, email: str, senha: str) -> Dict[str, Any]:
        """Registra um novo usuário"""
        response = requests.post(
            f'{self.base_url}/auth/registro',
            json={'nome': nome, 'email': email, 'senha': senha}
        )
        response.raise_for_status()
        return response.json()
    
    def criar_transacao(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova transação"""
        response = requests.post(
            f'{self.base_url}/transacoes',
            headers=self.get_headers(),
            json=dados
        )
        response.raise_for_status()
        return response.json()
    
    def listar_transacoes(self, filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Lista todas as transações"""
        response = requests.get(
            f'{self.base_url}/transacoes',
            headers=self.get_headers(),
            params=filtros
        )
        response.raise_for_status()
        return response.json()
    
    def atualizar_transacao(self, id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma transação existente"""
        response = requests.put(
            f'{self.base_url}/transacoes/{id}',
            headers=self.get_headers(),
            json=dados
        )
        response.raise_for_status()
        return response.json()
    
    def deletar_transacao(self, id: int) -> Dict[str, Any]:
        """Deleta uma transação"""
        response = requests.delete(
            f'{self.base_url}/transacoes/{id}',
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def listar_categorias(self) -> Dict[str, Any]:
        """Lista todas as categorias"""
        response = requests.get(
            f'{self.base_url}/categorias',
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def criar_categoria(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova categoria"""
        response = requests.post(
            f'{self.base_url}/categorias',
            headers=self.get_headers(),
            json=dados
        )
        response.raise_for_status()
        return response.json()
    
    def obter_relatorio_fluxo(self, filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Obtém o relatório de fluxo de caixa"""
        response = requests.get(
            f'{self.base_url}/relatorios/fluxo',
            headers=self.get_headers(),
            params=filtros
        )
        response.raise_for_status()
        return response.json()
    
    def obter_relatorio_categorias(self, filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Obtém o relatório por categorias"""
        response = requests.get(
            f'{self.base_url}/relatorios/categorias',
            headers=self.get_headers(),
            params=filtros
        )
        response.raise_for_status()
        return response.json() 