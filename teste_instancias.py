#!/usr/bin/env python3
"""
Teste das Instâncias Evolution API
Verifica instâncias disponíveis e suas configurações
"""

import requests
import json
from config import EvolutionAPIConfig

def main():
    print("=== TESTE DE INSTÂNCIAS EVOLUTION API ===\n")
    
    config = EvolutionAPIConfig()
    
    print(f"🌐 Servidor: {config.BASE_URL}")
    print(f"🔑 API Key: {config.API_KEY[:20]}...")
    print(f"📱 Instância Configurada: {config.INSTANCE_ID}")
    print("-" * 50)
    
    # Testar servidor local
    try:
        print("📡 Testando servidor local...")
        response = requests.get("http://localhost:8000/api/list-instances", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Sucesso! {data['total_instances']} instância(s) encontrada(s)")
                print(f"📋 Instância atual: {data['current_instance']}")
                print()
                
                for i, instance in enumerate(data['instances'], 1):
                    status_icon = "🟢" if instance['is_connected'] else "🔴"
                    print(f"{i}. {status_icon} {instance['instance_name']}")
                    print(f"   Status: {instance['connection_status']}")
                    print(f"   Perfil: {instance['profile_name']}")
                    print(f"   Telefone: {instance['phone_number']}")
                    print(f"   Conectado: {'Sim' if instance['is_connected'] else 'Não'}")
                    print()
                    
            else:
                print(f"❌ Erro: {data.get('error', 'Desconhecido')}")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor local não está rodando!")
        print("💡 Execute: uvicorn main:app --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main() 