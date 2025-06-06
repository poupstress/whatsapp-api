# Configurações da Evolution API v2
import os
from dotenv import load_dotenv

load_dotenv()

class EvolutionAPIConfig:
    """Configurações para integração com Evolution API"""
    
    # Configurações fornecidas pelo usuário
    SERVER_URL = "evolution.rdragentes.com.br"
    INSTANCE_ID = "rodolfo"
    API_KEY = "75363EE38AA4-438F-84AB-B870ACF55495"
    
    # URLs da API
    BASE_URL = f"https://{SERVER_URL}"
    SEND_TEXT_URL = f"{BASE_URL}/message/sendText/{INSTANCE_ID}"
    
    # Headers padrão para requisições
    HEADERS = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

# Configurações do servidor
class ServerConfig:
    """Configurações do servidor FastAPI"""
    
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True 