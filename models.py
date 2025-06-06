from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class ContactInfo(BaseModel):
    """Modelo para informações de contato"""
    name: str = Field(..., description="Nome do contato")
    phone: str = Field(..., description="Número do telefone com código do país")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Valida o formato do número de telefone"""
        # Remove espaços e caracteres especiais
        phone_clean = re.sub(r'[^\d+]', '', v)
        
        # Verifica se tem o código do país
        if not phone_clean.startswith('+'):
            # Assume código do Brasil se não especificado
            phone_clean = '+55' + phone_clean
        
        # Verifica se o número tem pelo menos 10 dígitos (sem código do país)
        digits_only = re.sub(r'[^\d]', '', phone_clean)
        if len(digits_only) < 10:
            raise ValueError('Número de telefone deve ter pelo menos 10 dígitos')
        
        return phone_clean

class BulkMessageRequest(BaseModel):
    """Modelo para requisição de envio em massa"""
    contacts: List[ContactInfo] = Field(..., description="Lista de contatos")
    message: str = Field(..., description="Mensagem a ser enviada")
    delay: Optional[int] = Field(1000, description="Delay entre mensagens em milissegundos")

class SingleMessageRequest(BaseModel):
    """Modelo para requisição de mensagem individual"""
    name: str = Field(..., description="Nome do destinatário")
    phone: str = Field(..., description="Número do telefone")
    message: str = Field(..., description="Mensagem a ser enviada")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Valida o formato do número de telefone"""
        phone_clean = re.sub(r'[^\d+]', '', v)
        
        if not phone_clean.startswith('+'):
            phone_clean = '+55' + phone_clean
        
        digits_only = re.sub(r'[^\d]', '', phone_clean)
        if len(digits_only) < 10:
            raise ValueError('Número de telefone deve ter pelo menos 10 dígitos')
        
        return phone_clean

class MessageResponse(BaseModel):
    """Modelo para resposta de envio de mensagem"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    sent_to: Optional[str] = None 