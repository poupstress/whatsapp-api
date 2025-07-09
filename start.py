#!/usr/bin/env python3
"""
Arquivo de inicialização simplificado para deploy no EasyPanel
"""

import os
import uvicorn

if __name__ == "__main__":
    # Configurações para deploy
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    print(f"🚀 Iniciando WhatsApp API em {host}:{port}")
    print(f"Workers: {workers}, Log Level: {log_level}")
    
    # Iniciar servidor
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        access_log=True
    ) 