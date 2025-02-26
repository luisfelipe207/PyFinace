import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'uj0xj.h.filess.io')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3305')
    MYSQL_USER = os.getenv('MYSQL_USER', 'PyFinance_simpleherd')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'd09f7f60a1620f49fe506fcd3a8f987d8b2ff880')
    MYSQL_DB = os.getenv('MYSQL_DB', 'PyFinance_simpleherd')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-chave-secreta')
    
    # String de conexão SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mariadb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 1,  # Limitar o pool a 1 conexão
        'max_overflow': 0,  # Não permitir conexões adicionais
        'pool_timeout': 30,  # Tempo de espera para uma conexão disponível
    } 