import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from config import EvolutionAPIConfig
from models import MessageResponse, BulkMessageRequest

# Configurar logger
logger = logging.getLogger(__name__)

class WhatsAppService:
    """Serviço para integração com Evolution API"""
    
    def __init__(self):
        self.config = EvolutionAPIConfig()
    
    def format_message(self, name: str, message: str) -> str:
        """
        Formata a mensagem com nome e data/hora atual
        Formato: Olá [Nome]
                [Mensagem]
                
                [Data e hora atual]
        """
        current_datetime = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        formatted_message = f"""Olá {name}!

{message}

{current_datetime}"""
        
        return formatted_message
    
    def send_message(self, phone: str, text: str) -> MessageResponse:
        """
        Envia mensagem individual via Evolution API
        
        Args:
            phone: Número do telefone (formato: +5511999999999)
            text: Texto da mensagem formatada
            
        Returns:
            MessageResponse: Resposta do envio
        """
        try:
            # Remove o + do número para a API
            clean_phone = phone.replace('+', '')
            
            # Payload conforme documentação da Evolution API
            payload = {
                "number": clean_phone,
                "text": text,
                "delay": 1000,
                "linkPreview": False,
                "mentionsEveryOne": False
            }
            
            logger.info(f"Enviando mensagem para {phone}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Fazer requisição para Evolution API
            response = requests.post(
                url=self.config.SEND_TEXT_URL,
                json=payload,
                headers=self.config.HEADERS,
                timeout=30
            )
            
            logger.info(f"Status da resposta: {response.status_code}")
            logger.debug(f"Resposta: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                return MessageResponse(
                    success=True,
                    message_id=response_data.get('key', {}).get('id'),
                    sent_to=phone
                )
            else:
                error_msg = f"Erro HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                return MessageResponse(
                    success=False,
                    error=error_msg,
                    sent_to=phone
                )
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout na requisição para Evolution API"
            logger.error(error_msg)
            return MessageResponse(
                success=False,
                error=error_msg,
                sent_to=phone
            )
        except requests.exceptions.ConnectionError:
            error_msg = "Erro de conexão com Evolution API"
            logger.error(error_msg)
            return MessageResponse(
                success=False,
                error=error_msg,
                sent_to=phone
            )
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            logger.error(error_msg)
            return MessageResponse(
                success=False,
                error=error_msg,
                sent_to=phone
            )
    
    def send_bulk_messages(self, request: BulkMessageRequest) -> Dict[str, Any]:
        """
        Envia mensagens em massa com delay configurável
        
        Args:
            request: Dados da requisição em massa
            
        Returns:
            Dict: Resultado do envio em massa
        """
        results = []
        successful = 0
        failed = 0
        
        for contact in request.contacts:
            try:
                # Formatar mensagem para cada contato
                formatted_message = self.format_message(contact.name, request.message)
                
                # Enviar mensagem
                result = self.send_message(contact.phone, formatted_message)
                
                if result.success:
                    successful += 1
                else:
                    failed += 1
                
                results.append({
                    "name": contact.name,
                    "phone": contact.phone,
                    "success": result.success,
                    "message_id": result.message_id,
                    "error": result.error
                })
                
                # Delay entre mensagens se não for a última
                if contact != request.contacts[-1] and request.delay > 0:
                    import time
                    time.sleep(request.delay / 1000)  # Converter para segundos
                    
            except Exception as e:
                failed += 1
                results.append({
                    "name": contact.name,
                    "phone": contact.phone,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "total_contacts": len(request.contacts),
            "successful": successful,
            "failed": failed,
            "results": results
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Testa a conexão com a Evolution API
        
        Returns:
            Dict: Status da conexão
        """
        try:
            # URL para testar conexão (usando endpoint de informações da instância)
            test_url = f"{self.config.BASE_URL}/instance/connect/{self.config.INSTANCE_ID}"
            
            response = requests.get(
                url=test_url,
                headers=self.config.HEADERS,
                timeout=10
            )
            
            return {
                "success": response.status_code in [200, 201],
                "status_code": response.status_code,
                "response": response.text[:200] if response.text else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_instance_status(self) -> Dict[str, Any]:
        """
        Obtém o status detalhado da instância WhatsApp
        
        Returns:
            Dict: Status detalhado da instância
        """
        try:
            # URL para obter status da instância
            status_url = f"{self.config.BASE_URL}/instance/fetchInstances"
            
            response = requests.get(
                url=status_url,
                headers=self.config.HEADERS,
                timeout=10
            )
            
            logger.info(f"Status da consulta: {response.status_code}")
            logger.debug(f"Resposta status: {response.text}")
            
            if response.status_code in [200, 201]:
                instances_data = response.json()
                
                # Procurar pela instância específica
                instance_info = None
                if isinstance(instances_data, list):
                    for instance in instances_data:
                        if instance.get('instance', {}).get('instanceName') == self.config.INSTANCE_ID:
                            instance_info = instance
                            break
                elif isinstance(instances_data, dict):
                    instance_info = instances_data
                
                if instance_info:
                    # Extrair informações relevantes
                    instance_data = instance_info.get('instance', {})
                    connection_status = instance_data.get('connectionStatus', 'unknown')
                    
                    return {
                        "success": True,
                        "instance_name": instance_data.get('instanceName'),
                        "connection_status": connection_status,
                        "is_connected": connection_status == 'open',
                        "profile_name": instance_data.get('profileName'),
                        "profile_picture": instance_data.get('profilePictureUrl'),
                        "phone_number": instance_data.get('number'),
                        "raw_response": instance_info
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Instância {self.config.INSTANCE_ID} não encontrada",
                        "available_instances": [inst.get('instance', {}).get('instanceName') for inst in instances_data if isinstance(instances_data, list)]
                    }
            else:
                return {
                    "success": False,
                    "error": f"Erro HTTP {response.status_code}: {response.text[:200]}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao obter status da instância: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_whatsapp_connection_status(self) -> Dict[str, Any]:
        """
        Verifica especificamente o status da conexão WhatsApp
        
        Returns:
            Dict: Status da conexão WhatsApp
        """
        try:
            # URL para verificar conexão WhatsApp
            connection_url = f"{self.config.BASE_URL}/instance/connectionState/{self.config.INSTANCE_ID}"
            
            response = requests.get(
                url=connection_url,
                headers=self.config.HEADERS,
                timeout=10
            )
            
            logger.info(f"Status da conexão WhatsApp: {response.status_code}")
            logger.debug(f"Resposta conexão: {response.text}")
            
            if response.status_code in [200, 201]:
                connection_data = response.json()
                return {
                    "success": True,
                    "connection_data": connection_data,
                    "is_whatsapp_connected": connection_data.get('instance', {}).get('state') == 'open'
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro HTTP {response.status_code}: {response.text[:200]}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao verificar conexão WhatsApp: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_all_instances(self) -> Dict[str, Any]:
        """
        Lista todas as instâncias disponíveis no Evolution API
        
        Returns:
            Dict: Lista de todas as instâncias com seus status
        """
        try:
            # URL para listar todas as instâncias
            instances_url = f"{self.config.BASE_URL}/instance/fetchInstances"
            
            response = requests.get(
                url=instances_url,
                headers=self.config.HEADERS,
                timeout=15
            )
            
            logger.info(f"Status da consulta de instâncias: {response.status_code}")
            logger.debug(f"Resposta instâncias: {response.text}")
            
            if response.status_code in [200, 201]:
                instances_data = response.json()
                
                # Processar dados das instâncias
                processed_instances = []
                
                if isinstance(instances_data, list):
                    for instance_raw in instances_data:
                        instance_data = instance_raw.get('instance', {})
                        
                        processed_instance = {
                            "instance_name": instance_data.get('instanceName', 'N/A'),
                            "connection_status": instance_data.get('connectionStatus', 'unknown'),
                            "is_connected": instance_data.get('connectionStatus') == 'open',
                            "profile_name": instance_data.get('profileName', 'N/A'),
                            "phone_number": instance_data.get('number', 'N/A'),
                            "profile_picture": instance_data.get('profilePictureUrl'),
                            "server_url": instance_data.get('serverUrl', 'N/A'),
                            "api_key": instance_data.get('apikey', 'N/A')[:20] + '...' if instance_data.get('apikey') else 'N/A',  # Mascarar API key
                            "created_at": instance_data.get('createdAt', 'N/A'),
                            "updated_at": instance_data.get('updatedAt', 'N/A')
                        }
                        
                        processed_instances.append(processed_instance)
                
                elif isinstance(instances_data, dict):
                    # Se retornar apenas uma instância
                    instance_data = instances_data.get('instance', {})
                    processed_instance = {
                        "instance_name": instance_data.get('instanceName', 'N/A'),
                        "connection_status": instance_data.get('connectionStatus', 'unknown'),
                        "is_connected": instance_data.get('connectionStatus') == 'open',
                        "profile_name": instance_data.get('profileName', 'N/A'),
                        "phone_number": instance_data.get('number', 'N/A'),
                        "profile_picture": instance_data.get('profilePictureUrl'),
                        "server_url": instance_data.get('serverUrl', 'N/A'),
                        "api_key": instance_data.get('apikey', 'N/A')[:20] + '...' if instance_data.get('apikey') else 'N/A',
                        "created_at": instance_data.get('createdAt', 'N/A'),
                        "updated_at": instance_data.get('updatedAt', 'N/A')
                    }
                    processed_instances.append(processed_instance)
                
                return {
                    "success": True,
                    "total_instances": len(processed_instances),
                    "current_instance": self.config.INSTANCE_ID,
                    "instances": processed_instances
                }
                
            else:
                return {
                    "success": False,
                    "error": f"Erro HTTP {response.status_code}: {response.text[:200]}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao listar instâncias: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            } 