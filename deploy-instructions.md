# 🚀 Instruções de Deploy - WhatsApp Message Manager

## 📋 Arquivos de Configuração Criados

### 1. **Variáveis de Ambiente**
- `env.example` - Modelo com todas as variáveis disponíveis
- `env.production` - Configurações otimizadas para produção
- `env.development` - Configurações para desenvolvimento local

### 2. **Docker (Opcional)**
- `Dockerfile` - Container otimizado para produção
- `docker-compose.yml` - Orquestração com Nginx

---

## 🔧 Como Configurar as Variáveis

### **Passo 1: Copiar arquivo de ambiente**
```bash
# Para produção
cp env.production .env

# Para desenvolvimento
cp env.development .env
```

### **Passo 2: Editar suas configurações**
Abra o arquivo `.env` e altere:

```bash
# SUAS CONFIGURAÇÕES DA EVOLUTION API
EVOLUTION_SERVER_URL=evolution.rdragentes.com.br
EVOLUTION_INSTANCE_ID=poupstress
EVOLUTION_API_KEY=0A2DB22449B7-4B21-9D31-CFDC55CA63E4

# SEU DOMÍNIO
DOMAIN=whatsapp-api.seudominio.com

# GERAR CHAVE SECRETA FORTE
SECRET_KEY=sua-chave-super-secreta-aqui
```

---

## 🌐 Deploy no EasyPanel

### **Opção 1: Deploy Direto (Sem Docker)**

1. **Configurar no EasyPanel:**
   - Fonte: GitHub
   - Repositório: `poupstress/whatsapp-api`
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Variáveis de Ambiente no EasyPanel:**
   ```bash
   EVOLUTION_SERVER_URL=evolution.rdragentes.com.br
   EVOLUTION_INSTANCE_ID=poupstress
   EVOLUTION_API_KEY=0A2DB22449B7-4B21-9D31-CFDC55CA63E4
   DEBUG=false
   HOST=0.0.0.0
   PORT=8000
   WORKERS=2
   LOG_LEVEL=warning
   ```

### **Opção 2: Deploy com Docker**

1. **Configurar no EasyPanel:**
   - Fonte: GitHub
   - Repositório: `poupstress/whatsapp-api`
   - Usar Dockerfile: ✅

2. **Variáveis de Ambiente:**
   ```bash
   EVOLUTION_SERVER_URL=evolution.rdragentes.com.br
   EVOLUTION_INSTANCE_ID=poupstress
   EVOLUTION_API_KEY=0A2DB22449B7-4B21-9D31-CFDC55CA63E4
   DEBUG=false
   WORKERS=2
   ```

---

## 🖥️ Deploy Manual na VPS

### **Preparar Servidor**
```bash
# Conectar via SSH
ssh usuario@sua-vps.com

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install python3 python3-pip python3-venv git nginx -y
```

### **Clonar e Configurar Projeto**
```bash
# Clonar repositório
git clone https://github.com/poupstress/whatsapp-api.git
cd whatsapp-api

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.production .env
nano .env  # Editar suas configurações
```

### **Criar Serviço Systemd**
```bash
sudo nano /etc/systemd/system/whatsapp-api.service
```

```ini
[Unit]
Description=WhatsApp Message Manager API
After=network.target

[Service]
Type=exec
User=usuario
WorkingDirectory=/home/usuario/whatsapp-api
Environment=PATH=/home/usuario/whatsapp-api/venv/bin
EnvironmentFile=/home/usuario/whatsapp-api/.env
ExecStart=/home/usuario/whatsapp-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **Iniciar Serviço**
```bash
sudo systemctl daemon-reload
sudo systemctl enable whatsapp-api
sudo systemctl start whatsapp-api
sudo systemctl status whatsapp-api
```

---

## 🔒 Configurar Nginx (Recomendado)

### **Criar configuração Nginx**
```bash
sudo nano /etc/nginx/sites-available/whatsapp-api
```

```nginx
server {
    listen 80;
    server_name whatsapp-api.seudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Ativar site**
```bash
sudo ln -s /etc/nginx/sites-available/whatsapp-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### **Configurar SSL**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d whatsapp-api.seudominio.com
```

---

## 🐳 Deploy com Docker

### **Usando Docker Compose**
```bash
# Configurar variáveis
cp env.production .env

# Subir serviços
docker-compose up -d

# Ver logs
docker-compose logs -f whatsapp-api
```

### **Apenas Docker**
```bash
# Build da imagem
docker build -t whatsapp-api .

# Executar container
docker run -d \
  --name whatsapp-api \
  --env-file .env \
  -p 8000:8000 \
  --restart unless-stopped \
  whatsapp-api
```

---

## 🔍 Verificar Deploy

### **Testar API**
```bash
# Health check
curl https://whatsapp-api.seudominio.com/api/health

# Teste de conexão
curl https://whatsapp-api.seudominio.com/api/test-connection

# Interface web
# Acesse: https://whatsapp-api.seudominio.com
```

### **Ver logs**
```bash
# Systemd
sudo journalctl -u whatsapp-api -f

# Docker
docker logs -f whatsapp-api

# Docker Compose
docker-compose logs -f
```

---

## 🔄 Atualizar Aplicação

### **Via Git**
```bash
cd /home/usuario/whatsapp-api
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart whatsapp-api
```

### **Via Docker**
```bash
docker-compose pull
docker-compose up -d
```

---

## 🛠️ Troubleshooting

### **Problemas Comuns**

1. **Erro de conexão Evolution API**
   - Verificar `EVOLUTION_SERVER_URL`
   - Verificar `EVOLUTION_API_KEY`
   - Testar: `curl https://evolution.rdragentes.com.br`

2. **Aplicação não inicia**
   - Verificar logs: `sudo journalctl -u whatsapp-api`
   - Verificar arquivo `.env`
   - Verificar permissões

3. **Erro 502 Bad Gateway**
   - Verificar se aplicação está rodando: `sudo systemctl status whatsapp-api`
   - Verificar configuração Nginx
   - Verificar firewall

### **Comandos Úteis**
```bash
# Status do serviço
sudo systemctl status whatsapp-api

# Reiniciar serviço
sudo systemctl restart whatsapp-api

# Ver logs em tempo real
sudo journalctl -u whatsapp-api -f

# Testar configuração Nginx
sudo nginx -t

# Verificar portas abertas
sudo netstat -tlnp | grep :8000
```

---

## 📞 Suporte

Se encontrar problemas:
1. Verificar logs da aplicação
2. Verificar configurações no arquivo `.env`
3. Testar conexão com Evolution API
4. Verificar firewall e portas

**Endpoints importantes:**
- Health: `/api/health`
- Docs: `/docs`
- Test: `/api/test-connection` 