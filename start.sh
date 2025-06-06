#!/bin/bash

# ==========================================
# Script de Inicialização WhatsApp API
# ==========================================

set -e  # Parar em caso de erro

echo "🚀 Iniciando WhatsApp Message Manager..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Detectar ambiente
detect_environment() {
    if [ -f /.dockerenv ]; then
        echo "docker"
    elif [ "$EASYPANEL" = "true" ] || [ "$VERCEL" = "1" ] || [ "$RAILWAY_ENVIRONMENT" != "" ]; then
        echo "cloud"
    elif [ "$USER" = "root" ] || [ "$HOME" = "/root" ]; then
        echo "vps"
    else
        echo "local"
    fi
}

# Configurar variáveis baseado no ambiente
setup_environment() {
    local env_type=$(detect_environment)
    
    log_info "Ambiente detectado: $env_type"
    
    case $env_type in
        "docker")
            export HOST=${HOST:-"0.0.0.0"}
            export PORT=${PORT:-8000}
            log_info "Configuração Docker aplicada"
            ;;
        "cloud")
            export HOST=${HOST:-"0.0.0.0"}
            export PORT=${PORT:-8000}
            export DEBUG=${DEBUG:-"false"}
            log_info "Configuração Cloud aplicada"
            ;;
        "vps")
            export HOST=${HOST:-"0.0.0.0"}
            export PORT=${PORT:-8000}
            export DEBUG=${DEBUG:-"false"}
            log_info "Configuração VPS aplicada"
            ;;
        "local")
            export HOST=${HOST:-"127.0.0.1"}
            export PORT=${PORT:-8000}
            export DEBUG=${DEBUG:-"true"}
            log_info "Configuração Local aplicada"
            ;;
    esac
}

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 não encontrado!"
        exit 1
    fi
    
    # Verificar pip
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        log_error "pip não encontrado!"
        exit 1
    fi
    
    # Verificar uvicorn
    if ! python3 -c "import uvicorn" 2>/dev/null; then
        log_warning "uvicorn não encontrado, instalando dependências..."
        pip install -r requirements.txt
    fi
    
    log_success "Dependências verificadas"
}

# Carregar variáveis de ambiente
load_env_vars() {
    log_info "Carregando variáveis de ambiente..."
    
    # Tentar carregar arquivo .env
    if [ -f ".env" ]; then
        log_info "Carregando .env"
        export $(cat .env | grep -v '^#' | xargs)
    elif [ -f "env.production" ]; then
        log_warning ".env não encontrado, usando env.production"
        export $(cat env.production | grep -v '^#' | xargs)
    elif [ -f "env.development" ]; then
        log_warning ".env não encontrado, usando env.development"
        export $(cat env.development | grep -v '^#' | xargs)
    else
        log_warning "Nenhum arquivo de ambiente encontrado, usando padrões"
    fi
}

# Validar configurações
validate_config() {
    log_info "Validando configurações..."
    
    local errors=0
    
    if [ -z "$EVOLUTION_SERVER_URL" ]; then
        log_error "EVOLUTION_SERVER_URL não definida"
        errors=$((errors + 1))
    fi
    
    if [ -z "$EVOLUTION_INSTANCE_ID" ]; then
        log_error "EVOLUTION_INSTANCE_ID não definida"
        errors=$((errors + 1))
    fi
    
    if [ -z "$EVOLUTION_API_KEY" ]; then
        log_error "EVOLUTION_API_KEY não definida"
        errors=$((errors + 1))
    fi
    
    if [ $errors -gt 0 ]; then
        log_error "Configuração inválida! Verifique as variáveis de ambiente."
        exit 1
    fi
    
    log_success "Configuração válida"
}

# Testar conexão com Evolution API
test_evolution_connection() {
    log_info "Testando conexão com Evolution API..."
    
    local url="https://${EVOLUTION_SERVER_URL}"
    
    if command -v curl &> /dev/null; then
        if curl -s --connect-timeout 10 "$url" > /dev/null; then
            log_success "Conexão com Evolution API OK"
        else
            log_warning "Não foi possível conectar com Evolution API"
        fi
    else
        log_warning "curl não disponível, pulando teste de conexão"
    fi
}

# Criar diretórios necessários
create_directories() {
    log_info "Criando diretórios necessários..."
    
    mkdir -p logs
    mkdir -p static
    mkdir -p templates
    
    log_success "Diretórios criados"
}

# Mostrar informações de inicialização
show_startup_info() {
    echo ""
    echo "=================================="
    echo "🚀 WhatsApp Message Manager"
    echo "=================================="
    echo "Host: $HOST"
    echo "Porta: $PORT"
    echo "Debug: ${DEBUG:-false}"
    echo "Workers: ${WORKERS:-1}"
    echo "Log Level: ${LOG_LEVEL:-info}"
    echo "Evolution API: $EVOLUTION_SERVER_URL"
    echo "Instância: $EVOLUTION_INSTANCE_ID"
    echo "=================================="
    echo ""
}

# Função principal
main() {
    # Executar verificações
    setup_environment
    load_env_vars
    check_dependencies
    validate_config
    test_evolution_connection
    create_directories
    show_startup_info
    
    # Definir valores padrão finais
    HOST=${HOST:-"0.0.0.0"}
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-1}
    LOG_LEVEL=${LOG_LEVEL:-"info"}
    
    # Iniciar aplicação
    log_success "Iniciando aplicação..."
    
    exec uvicorn main:app \
        --host "$HOST" \
        --port "$PORT" \
        --workers "$WORKERS" \
        --log-level "$LOG_LEVEL" \
        --access-log
}

# Tratamento de sinais
trap 'log_warning "Recebido sinal de parada, finalizando..."; exit 0' SIGTERM SIGINT

# Executar função principal
main "$@" 