#!/usr/bin/env python3
"""
Configurador de API Key - Evolution API
Permite testar e configurar diferentes API keys
"""

import requests
import json

def test_api_key(api_key, server_url="https://evolution.rdragentes.com.br"):
    """Testa uma API key específica"""
    print(f"🔑 Testando API Key: {api_key[:20]}...")
    
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    
    test_urls = [
        f"{server_url}/instance/fetchInstances",
        f"{server_url}/instance/connect/PoupStress",
        f"{server_url}/message/sendText/PoupStress"
    ]
    
    results = {}
    
    for url in test_urls:
        endpoint = url.split('/')[-1] if url.split('/')[-1] else url.split('/')[-2]
        
        try:
            if "sendText" in url:
                # Para teste de envio, usar POST
                response = requests.post(url, headers=headers, json={"number": "5531999999999", "text": "teste"}, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                results[endpoint] = "✅ OK"
                if "fetchInstances" in url:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            results[endpoint] += f" ({len(data)} instâncias)"
                        elif isinstance(data, dict) and 'instance' in data:
                            results[endpoint] += " (1 instância)"
                    except:
                        pass
            elif response.status_code == 401:
                results[endpoint] = "❌ 401 Unauthorized"
            elif response.status_code == 403:
                results[endpoint] = "❌ 403 Forbidden"
            elif response.status_code == 404:
                results[endpoint] = "❌ 404 Not Found"
            else:
                results[endpoint] = f"❌ {response.status_code}"
                
        except Exception as e:
            results[endpoint] = f"❌ Erro: {str(e)[:30]}"
    
    return results

def main():
    print("=== CONFIGURADOR DE API KEY EVOLUTION API ===\n")
    
    # API Keys para testar (você pode adicionar mais)
    api_keys_to_test = [
        "62D811330286-4F48-B836-8FE1955A8A1F",  # Atual
        # Adicione outras API keys aqui se tiver
    ]
    
    server_url = "https://evolution.rdragentes.com.br"
    
    print(f"🌐 Servidor: {server_url}")
    print(f"📱 Instância: PoupStress")
    print("-" * 60)
    
    valid_keys = []
    
    for i, api_key in enumerate(api_keys_to_test, 1):
        print(f"\n🔍 Teste {i}:")
        results = test_api_key(api_key, server_url)
        
        for endpoint, result in results.items():
            print(f"   {endpoint}: {result}")
        
        # Verificar se a key é válida
        if any("✅" in result for result in results.values()):
            valid_keys.append(api_key)
            print(f"   ✅ Esta API Key funciona!")
        else:
            print(f"   ❌ Esta API Key não funciona")
    
    print("\n" + "="*60)
    
    if valid_keys:
        print(f"✅ {len(valid_keys)} API Key(s) válida(s) encontrada(s):")
        for key in valid_keys:
            print(f"   🔑 {key}")
        
        # Atualizar config.py automaticamente
        if len(valid_keys) == 1:
            update_config = input(f"\n🔧 Deseja atualizar config.py com a API Key válida? (s/N): ")
            if update_config.lower() == 's':
                update_config_file(valid_keys[0])
    else:
        print("❌ Nenhuma API Key válida encontrada!")
        print("\n💡 Próximos passos:")
        print("   1. Verifique se a API Key está correta")
        print("   2. Confirme as permissões no painel Evolution")
        print("   3. Gere uma nova API Key se necessário")
        print("   4. Verifique se a instância 'PoupStress' existe")

def update_config_file(api_key):
    """Atualiza o arquivo config.py com a nova API key"""
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir a API key
        import re
        pattern = r'API_KEY = "[^"]*"'
        new_content = re.sub(pattern, f'API_KEY = "{api_key}"', content)
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ config.py atualizado com sucesso!")
        print("🔄 Reinicie o servidor para aplicar as mudanças")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar config.py: {e}")

if __name__ == "__main__":
    main()
    
    print(f"\n📝 Para adicionar mais API Keys para teste:")
    print(f"   Edite este arquivo e adicione as keys na lista 'api_keys_to_test'")
    
    print(f"\n🔧 Para testar manualmente:")
    print(f"   python configurar_apikey.py") 