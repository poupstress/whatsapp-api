FROM python:3.11-slim

# Metadados
LABEL maintainer="seu-email@exemplo.com"
LABEL version="1.0.0"
LABEL description="WhatsApp Message Manager API"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements primeiro (para melhor cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Variáveis de ambiente padrão (podem ser sobrescritas)
ENV HOST=0.0.0.0
ENV PORT=8000
ENV WORKERS=1
ENV LOG_LEVEL=info
ENV DEBUG=false

# Expor porta
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# Comando para iniciar a aplicação
CMD uvicorn main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --log-level $LOG_LEVEL 