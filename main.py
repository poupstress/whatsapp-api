from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import json
import logging
from datetime import datetime
import os

from models import BulkMessageRequest, SingleMessageRequest, MessageResponse, ContactInfo
from whatsapp_service import WhatsAppService
from config import ServerConfig

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obter path prefix da variável de ambiente
ROOT_PATH = os.getenv("ROOT_PATH", "").rstrip("/")

# Inicializar FastAPI com root_path para subdiretórios
app = FastAPI(
    title="WhatsApp Message Manager",
    description="Sistema de gerenciamento de mensagens WhatsApp usando Evolution API",
    version="1.0.0",
    root_path=ROOT_PATH,  # Suporte para subdiretórios
    docs_url="/docs" if not ROOT_PATH else f"{ROOT_PATH}/docs",
    redoc_url="/redoc" if not ROOT_PATH else f"{ROOT_PATH}/redoc",
    openapi_url="/openapi.json" if not ROOT_PATH else f"{ROOT_PATH}/openapi.json"
)

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializar serviço WhatsApp
whatsapp_service = WhatsAppService()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página inicial do frontend"""
    # Passar informações do path para o template
    context = {
        "request": request,
        "root_path": ROOT_PATH,
        "api_base_url": f"{ROOT_PATH}/api" if ROOT_PATH else "/api"
    }
    return templates.TemplateResponse("index.html", context)

@app.post("/api/send-message", response_model=MessageResponse)
async def send_single_message(message_data: SingleMessageRequest):
    """
    Endpoint para envio de mensagem individual
    Usado pelo frontend e pode ser chamado externamente
    """
    try:
        # Formatar mensagem personalizada
        formatted_message = whatsapp_service.format_message(
            name=message_data.name,
            message=message_data.message
        )
        
        # Enviar mensagem
        result = whatsapp_service.send_message(
            phone=message_data.phone,
            text=formatted_message
        )
        
        logger.info(f"Mensagem enviada para {message_data.name} ({message_data.phone}): {result.success}")
        return result
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem individual: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/api/send-bulk-messages")
async def send_bulk_messages(bulk_data: BulkMessageRequest):
    """
    Endpoint principal para envio em massa
    Este é o endpoint que será chamado pelo sistema PHP
    """
    try:
        logger.info(f"Iniciando envio em massa para {len(bulk_data.contacts)} contatos")
        
        # Enviar mensagens em massa
        results = whatsapp_service.send_bulk_messages(bulk_data)
        
        logger.info(f"Envio em massa concluído: {results['successful']} sucessos, {results['failed']} falhas")
        return {
            "success": True,
            "total_contacts": results['total_contacts'],
            "successful_sends": results['successful'],
            "failed_sends": results['failed'],
            "results": results['results']
        }
        
    except Exception as e:
        logger.error(f"Erro no envio em massa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/api/send-bulk-form")
async def send_bulk_form_data(
    request: Request,
    message: str = Form(...),
    contacts_json: str = Form(...)
):
    """
    Endpoint para envio em massa via formulário do frontend
    Recebe dados do formulário HTML
    """
    try:
        # Parsear JSON dos contatos
        contacts_data = json.loads(contacts_json)
        
        # Validar e converter para modelo Pydantic
        contacts = [ContactInfo(**contact) for contact in contacts_data]
        
        # Criar requisição
        bulk_request = BulkMessageRequest(
            contacts=contacts,
            message=message,
            delay=1000
        )
        
        # Reutilizar lógica do endpoint principal
        return await send_bulk_messages(bulk_request)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON dos contatos inválido")
    except Exception as e:
        logger.error(f"Erro no formulário de envio em massa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/test-connection")
async def test_connection():
    """Testar conexão com Evolution API"""
    try:
        result = whatsapp_service.test_connection()
        return result
    except Exception as e:
        logger.error(f"Erro ao testar conexão: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/instance-status")
async def get_instance_status():
    """Obter status detalhado da instância WhatsApp"""
    try:
        result = whatsapp_service.get_instance_status()
        return result
    except Exception as e:
        logger.error(f"Erro ao obter status da instância: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/whatsapp-connection")
async def get_whatsapp_connection():
    """Verificar conexão específica do WhatsApp"""
    try:
        result = whatsapp_service.get_whatsapp_connection_status()
        return result
    except Exception as e:
        logger.error(f"Erro ao verificar conexão WhatsApp: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/full-diagnosis")
async def full_diagnosis():
    """Diagnóstico completo do sistema"""
    try:
        # Coletar todas as informações de diagnóstico
        connection_test = whatsapp_service.test_connection()
        instance_status = whatsapp_service.get_instance_status()
        whatsapp_connection = whatsapp_service.get_whatsapp_connection_status()
        
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "evolution_api_connection": connection_test,
            "instance_status": instance_status,
            "whatsapp_connection": whatsapp_connection,
            "summary": {
                "api_reachable": connection_test.get("success", False),
                "instance_found": instance_status.get("success", False),
                "whatsapp_connected": False,
                "issues": []
            }
        }
        
        # Analisar problemas
        if not connection_test.get("success"):
            diagnosis["summary"]["issues"].append("Evolution API não está acessível")
        
        if not instance_status.get("success"):
            diagnosis["summary"]["issues"].append("Instância não encontrada ou com erro")
        elif not instance_status.get("is_connected"):
            diagnosis["summary"]["issues"].append("Instância não está conectada ao WhatsApp")
            
        if not whatsapp_connection.get("success"):
            diagnosis["summary"]["issues"].append("Erro ao verificar conexão WhatsApp")
        elif not whatsapp_connection.get("is_whatsapp_connected"):
            diagnosis["summary"]["issues"].append("WhatsApp não está conectado")
        else:
            diagnosis["summary"]["whatsapp_connected"] = True
        
        return diagnosis
        
    except Exception as e:
        logger.error(f"Erro no diagnóstico completo: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/list-instances")
async def list_instances():
    """Listar todas as instâncias disponíveis no Evolution API"""
    try:
        result = whatsapp_service.list_all_instances()
        return result
    except Exception as e:
        logger.error(f"Erro ao listar instâncias: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/health")
async def health_check():
    """
    Health check da aplicação
    """
    return {
        "status": "healthy",
        "service": "WhatsApp Message Manager",
        "version": "1.0.0"
    }

# Exemplo de uso para integração PHP
@app.get("/api/example")
async def example_usage():
    """
    Retorna exemplo de como usar a API
    """
    return {
        "message": "Exemplo de uso da API",
        "endpoints": {
            "send_bulk": {
                "url": "/api/send-bulk-messages",
                "method": "POST",
                "example_payload": {
                    "contacts": [
                        {"name": "João Silva", "phone": "+5511999999999"},
                        {"name": "Maria Santos", "phone": "+5511888888888"}
                    ],
                    "message": "Esta é uma mensagem de teste!",
                    "delay": 1000
                }
            },
            "send_single": {
                "url": "/api/send-message",
                "method": "POST",
                "example_payload": {
                    "name": "João Silva",
                    "phone": "+5511999999999",
                    "message": "Mensagem individual de teste"
                }
            }
        },
        "php_integration_example": """
// Exemplo de código PHP para integração
$data = [
    'contacts' => [
        ['name' => 'João Silva', 'phone' => '+5511999999999'],
        ['name' => 'Maria Santos', 'phone' => '+5511888888888']
    ],
    'message' => 'Sua mensagem aqui',
    'delay' => 1000
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://localhost:8000/api/send-bulk-messages');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

echo $response;
        """
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Iniciando servidor WhatsApp Message Manager...")
    logger.info(f"Acesse: http://{ServerConfig.HOST}:{ServerConfig.PORT}")
    logger.info(f"Documentação: http://{ServerConfig.HOST}:{ServerConfig.PORT}/docs")
    
    uvicorn.run(
        app,
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        reload=ServerConfig.DEBUG
    ) 