# Configurações da Evolution API v2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class EvolutionAPIConfig:
    """Configurações para integração com Evolution API"""
    
    # Configurações da Evolution API - agora usando variáveis de ambiente
    SERVER_URL = os.getenv("EVOLUTION_SERVER_URL", "evolution.rdragentes.com.br")
    INSTANCE_ID = os.getenv("EVOLUTION_INSTANCE_ID", "rodolfo")
    API_KEY = os.getenv("EVOLUTION_API_KEY", "75363EE38AA4-438F-84AB-B870ACF55495")
    
    # URLs da API
    BASE_URL = f"https://{SERVER_URL}"
    SEND_TEXT_URL = f"{BASE_URL}/message/sendText/{INSTANCE_ID}"
    
    # Headers padrão para requisições
    HEADERS = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Configurações de timeout e delay
    HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 30))
    DEFAULT_MESSAGE_DELAY = int(os.getenv("DEFAULT_MESSAGE_DELAY", 1000))

class ServerConfig:
    """Configurações do servidor FastAPI"""
    
    # Configurações básicas do servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    WORKERS = int(os.getenv("WORKERS", 1))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Configurações de domínio e CORS
    DOMAIN = os.getenv("DOMAIN", "localhost")
    ALLOW_CORS_ALL = os.getenv("ALLOW_CORS_ALL", "false").lower() == "true"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
    
    # Configurações de segurança
    SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-padrao-mude-em-producao")
    
    # Configurações de monitoramento
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "false").lower() == "true"
    HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", 60))

class DatabaseConfig:
    """Configurações de banco de dados (opcional)"""
    
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    REDIS_URL = os.getenv("REDIS_URL", None)

class EmailConfig:
    """Configurações de email (opcional)"""
    
    SMTP_HOST = os.getenv("SMTP_HOST", None)
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587)) if os.getenv("SMTP_PORT") else None
    SMTP_USER = os.getenv("SMTP_USER", None)
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", None)
    SMTP_FROM = os.getenv("SMTP_FROM", None)

# Função para validar configurações
def validate_config():
    """Valida se as configurações essenciais estão definidas"""
    errors = []
    
    if not EvolutionAPIConfig.SERVER_URL:
        errors.append("EVOLUTION_SERVER_URL não está definida")
    
    if not EvolutionAPIConfig.INSTANCE_ID:
        errors.append("EVOLUTION_INSTANCE_ID não está definida")
    
    if not EvolutionAPIConfig.API_KEY:
        errors.append("EVOLUTION_API_KEY não está definida")
    
    if ServerConfig.ENVIRONMENT == "production" and ServerConfig.SECRET_KEY == "sua-chave-secreta-padrao-mude-em-producao":
        errors.append("SECRET_KEY deve ser alterada em produção")
    
    if errors:
        raise ValueError("Erros de configuração:\n" + "\n".join(f"- {error}" for error in errors))
    
    return True

# Validar configurações ao importar
if __name__ != "__main__":
    try:
        validate_config()
    except ValueError as e:
        print(f"⚠️ Aviso de configuração: {e}") 