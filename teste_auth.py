#!/usr/bin/env python3
"""
Teste de Autenticação Evolution API
Testa diferentes formatos de autenticação
"""

import requests
import json
from config import EvolutionAPIConfig

def test_auth_methods():
    print("=== TESTE DE AUTENTICAÇÃO EVOLUTION API ===\n")
    
    config = EvolutionAPIConfig()
    
    print(f"🌐 Servidor: {config.BASE_URL}")
    print(f"🔑 API Key: {config.API_KEY}")
    print(f"📱 Instância: {config.INSTANCE_ID}")
    print("-" * 60)
    
    # URLs para testar
    test_urls = [
        f"{config.BASE_URL}/instance/fetchInstances",
        f"{config.BASE_URL}/instance/connect/{config.INSTANCE_ID}",
        f"{config.BASE_URL}/instance/connectionState/{config.INSTANCE_ID}",
        f"{config.BASE_URL}/health"
    ]
    
    # Formatos de headers para testar
    auth_formats = [
        {"apikey": config.API_KEY, "Content-Type": "application/json"},
        {"apiKey": config.API_KEY, "Content-Type": "application/json"},
        {"API-KEY": config.API_KEY, "Content-Type": "application/json"},
        {"Authorization": f"Bearer {config.API_KEY}", "Content-Type": "application/json"},
        {"Authorization": f"ApiKey {config.API_KEY}", "Content-Type": "application/json"},
        {"X-API-KEY": config.API_KEY, "Content-Type": "application/json"},
    ]
    
    print("📋 Testando diferentes formatos de autenticação...\n")
    
    for i, headers in enumerate(auth_formats, 1):
        print(f"🔍 Teste {i}: {list(headers.keys())[0]}")
        
        for url in test_urls:
            endpoint_name = url.split('/')[-1]
            print(f"   → {endpoint_name}: ", end="")
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print("✅ OK")
                    # Se encontrou um formato que funciona, mostrar detalhes
                    if "fetchInstances" in url:
                        try:
                            data = response.json()
                            if isinstance(data, list) and len(data) > 0:
                                print(f"      📋 {len(data)} instância(s) encontrada(s)")
                                for inst in data:
                                    inst_data = inst.get('instance', {})
                                    name = inst_data.get('instanceName', 'N/A')
                                    status = inst_data.get('connectionStatus', 'N/A')
                                    print(f"         • {name}: {status}")
                        except:
                            pass
                elif response.status_code == 401:
                    print("❌ 401 Unauthorized")
                elif response.status_code == 403:
                    print("❌ 403 Forbidden")
                elif response.status_code == 404:
                    print("❌ 404 Not Found")
                else:
                    print(f"❌ {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Conexão falhou")
            except requests.exceptions.Timeout:
                print("❌ Timeout")
            except Exception as e:
                print(f"❌ Erro: {str(e)[:30]}...")
        
        print()
    
    print("🔧 Testando endpoint de health/status...")
    # Testar endpoint básico sem autenticação
    try:
        simple_urls = [
            f"{config.BASE_URL}",
            f"{config.BASE_URL}/health",
            f"{config.BASE_URL}/status",
            f"{config.BASE_URL}/api/health"
        ]
        
        for url in simple_urls:
            try:
                response = requests.get(url, timeout=5)
                print(f"   {url}: {response.status_code}")
                if response.status_code == 200:
                    print(f"      Resposta: {response.text[:100]}...")
            except:
                print(f"   {url}: Falhou")
                
    except Exception as e:
        print(f"Erro nos testes básicos: {e}")

if __name__ == "__main__":
    test_auth_methods() 