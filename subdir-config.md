# 📁 Configuração para Subdiretório - dominio.com/whatsapp-api

## 🎯 Objetivo
Configurar a aplicação para funcionar em `dominio.com/whatsapp-api` em vez da raiz do domínio.

## ⚙️ Configurações Necessárias

### 1. **Variável de Ambiente ROOT_PATH**

Para usar em subdiretório, configure:
```bash
ROOT_PATH=/whatsapp-api
```

### 2. **Opções de Deploy**

#### **Opção A: EasyPanel com Nginx Próprio**
Se você tem controle total do servidor:

1. **Variáveis no EasyPanel:**
   ```bash
   ROOT_PATH=/whatsapp-api
   HOST=127.0.0.1
   PORT=8000
   ```

2. **Configurar Nginx** (usar arquivo `nginx.conf` fornecido)

#### **Opção B: EasyPanel com Proxy Automático**
Se o EasyPanel gerencia o proxy:

1. **Variáveis no EasyPanel:**
   ```bash
   ROOT_PATH=/whatsapp-api
   HOST=0.0.0.0
   PORT=8000
   ```

2. **Configurar Path no EasyPanel:**
   - Base Path: `/whatsapp-api`
   - ou Custom Domain: `dominio.com/whatsapp-api`

#### **Opção C: Deploy Manual com Nginx**
Para VPS própria:

1. **Usar arquivo env.production:**
   ```bash
   cp env.production .env
   # Editar .env se necessário
   ```

2. **Configurar Nginx:**
   ```bash
   sudo cp nginx.conf /etc/nginx/nginx.conf
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 🌐 URLs Resultantes

Com `ROOT_PATH=/whatsapp-api`, sua aplicação ficará:

- **Interface:** `https://dominio.com/whatsapp-api/`
- **API Docs:** `https://dominio.com/whatsapp-api/docs`
- **Health Check:** `https://dominio.com/whatsapp-api/api/health`
- **Enviar Mensagem:** `https://dominio.com/whatsapp-api/api/send-message`
- **Envio em Massa:** `https://dominio.com/whatsapp-api/api/send-bulk-messages`

## 📝 Exemplos de Chamada da API

### **PHP atualizado para subdiretório:**
```php
<?php
class WhatsAppClientSubdir {
    private $baseUrl;
    
    public function __construct($baseUrl = 'https://dominio.com/whatsapp-api') {
        $this->baseUrl = $baseUrl;
    }
    
    public function enviarMensagem($nome, $telefone, $mensagem) {
        $dados = [
            'name' => $nome,
            'phone' => $telefone,
            'message' => $mensagem
        ];
        
        return $this->fazerRequisicao('/api/send-message', $dados);
    }
    
    // ... resto do código igual
}

// Uso
$whatsapp = new WhatsAppClientSubdir('https://seudominio.com/whatsapp-api');
$resultado = $whatsapp->enviarMensagem('João', '+5511999999999', 'Teste');
```

### **JavaScript atualizado:**
```javascript
class WhatsAppClientSubdir {
    constructor(baseUrl = 'https://dominio.com/whatsapp-api') {
        this.baseUrl = baseUrl;
    }
    
    async enviarMensagem(nome, telefone, mensagem) {
        const response = await fetch(`${this.baseUrl}/api/send-message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: nome, phone: telefone, message: mensagem })
        });
        
        return await response.json();
    }
}

// Uso
const whatsapp = new WhatsAppClientSubdir('https://seudominio.com/whatsapp-api');
const resultado = await whatsapp.enviarMensagem('João', '+5511999999999', 'Teste');
```

### **cURL atualizado:**
```bash
# Teste de saúde
curl https://seudominio.com/whatsapp-api/api/health

# Enviar mensagem
curl -X POST https://seudominio.com/whatsapp-api/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "phone": "+5511999999999",
    "message": "Mensagem de teste"
  }'
```

## 🔧 Configuração Nginx Detalhada

O arquivo `nginx.conf` criado faz:

1. **Rewrite de URLs:** Remove `/whatsapp-api` antes de enviar para o backend
2. **Headers corretos:** Adiciona `X-Forwarded-Prefix` para o FastAPI
3. **Arquivos estáticos:** Serve corretamente CSS/JS
4. **Health checks:** Funciona em `/whatsapp-api/health`

### **Estrutura de URLs:**
```
https://dominio.com/                    → Página principal (opcional)
https://dominio.com/whatsapp-api/       → Interface WhatsApp
https://dominio.com/whatsapp-api/api/   → Endpoints da API
https://dominio.com/whatsapp-api/docs   → Documentação
```

## 🚀 Deploy Passo a Passo

### **1. Atualizar Variáveis:**
```bash
# No arquivo .env ou EasyPanel
ROOT_PATH=/whatsapp-api
```

### **2. Fazer Deploy:**
```bash
git add .
git commit -m "Configurar para subdiretório /whatsapp-api"
git push origin main
```

### **3. Configurar Proxy (se necessário):**
- **EasyPanel:** Configurar Custom Path
- **VPS Manual:** Usar nginx.conf fornecido

### **4. Testar:**
```bash
curl https://seudominio.com/whatsapp-api/api/health
```

## 🔍 Troubleshooting

### **Problema: 404 Not Found**
- Verificar se `ROOT_PATH` está configurado
- Verificar configuração do proxy/nginx
- Verificar se aplicação está rodando

### **Problema: CSS/JS não carrega**
- Verificar configuração de arquivos estáticos no nginx
- Verificar se `root_path` está sendo passado para templates

### **Problema: API retorna URLs erradas**
- Verificar se `ROOT_PATH` está definido corretamente
- Verificar se proxy está enviando headers corretos

## 📋 Checklist de Configuração

- [ ] `ROOT_PATH=/whatsapp-api` configurado
- [ ] Deploy realizado com sucesso
- [ ] Nginx configurado (se aplicável)
- [ ] Teste de health check funcionando
- [ ] Interface acessível em `/whatsapp-api/`
- [ ] API Docs acessível em `/whatsapp-api/docs`
- [ ] Clientes PHP/JS atualizados com nova URL base

## 🎯 Resultado Final

Sua aplicação estará disponível em:
- **🌐 Interface:** `https://seudominio.com/whatsapp-api/`
- **📚 Documentação:** `https://seudominio.com/whatsapp-api/docs`
- **🔍 Health Check:** `https://seudominio.com/whatsapp-api/api/health`

E você pode ter outros serviços na raiz do domínio ou em outros subdiretórios! 