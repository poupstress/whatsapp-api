# WhatsApp Message Manager

Sistema completo de gerenciamento de mensagens WhatsApp usando Evolution API v2, desenvolvido em Python com FastAPI e interface web moderna.

## 🚀 Funcionalidades

- **Backend API REST** para integração com sistemas PHP
- **Interface Web** para envio individual e em massa
- **Formatação automática** de mensagens com nome e data/hora
- **Validação** de números de telefone
- **Logs detalhados** de envios
- **Teste de conexão** com Evolution API
- **Design responsivo** e moderno

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta Evolution API configurada
- Navegador moderno para o frontend

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd Mensageria
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis no arquivo `config.py`

As configurações da Evolution API já estão definidas no arquivo `config.py`:

```python
# Configurações da Evolution API v2
SERVER_URL = "evolution.rdragentes.com.br"
INSTANCE_ID = "PoupStress"
API_KEY = "62D811330286-4F48-B836-8FE1955A8A1F"
```

### 4. Execute o servidor

```bash
python main.py
```

O servidor estará disponível em:
- **Interface Web**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/redoc

## 🌐 Usando a Interface Web

### Mensagem Individual
1. Acesse http://localhost:8000
2. Na aba "Mensagem Individual"
3. Preencha nome, telefone e mensagem
4. Clique em "Enviar Mensagem"

### Mensagem em Massa
1. Na aba "Mensagem em Massa"
2. Adicione contatos usando o formulário
3. Digite a mensagem
4. Clique em "Enviar Mensagens em Massa"

## 🔌 Integração PHP

### Endpoint para Envio em Massa

**URL**: `POST /api/send-bulk-messages`

**Exemplo de código PHP**:

```php
<?php
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

$result = json_decode($response, true);
echo "Sucessos: " . $result['successful_sends'];
echo "Falhas: " . $result['failed_sends'];
?>
```

### Endpoint para Mensagem Individual

**URL**: `POST /api/send-message`

**Exemplo de código PHP**:

```php
<?php
$data = [
    'name' => 'João Silva',
    'phone' => '+5511999999999',
    'message' => 'Mensagem individual de teste'
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://localhost:8000/api/send-message');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

$result = json_decode($response, true);
if ($result['success']) {
    echo "Mensagem enviada com sucesso!";
} else {
    echo "Erro: " . $result['error'];
}
?>
```

## 📊 Formato das Mensagens

As mensagens são automaticamente formatadas com:

```
Olá [Nome]!

[Sua mensagem]

[Data e hora atual]
```

**Exemplo**:
```
Olá João Silva!

Sua conta foi atualizada com sucesso.

04/06/2025 às 14:30
```

## 🔍 Endpoints da API

### Principal
- `POST /api/send-bulk-messages` - Envio em massa
- `POST /api/send-message` - Mensagem individual
- `GET /api/test-connection` - Testar conexão
- `GET /api/health` - Status da aplicação
- `GET /api/example` - Exemplos de uso

### Frontend
- `GET /` - Interface web principal
- `POST /api/send-bulk-form` - Envio via formulário

## 📱 Formato de Telefone

- **Aceito**: `+5511999999999`, `5511999999999`, `11999999999`
- **Convertido automaticamente** para: `+5511999999999`
- Deve ter no mínimo 10 dígitos (sem código do país)

## 🎨 Características do Frontend

- **Design moderno** com Bootstrap 5
- **Interface responsiva** para mobile
- **Feedback visual** em tempo real
- **Validação** de dados no cliente
- **Loading** com indicadores visuais
- **Alertas** informativos

## 🔧 Configurações Avançadas

### Arquivo config.py

```python
class EvolutionAPIConfig:
    SERVER_URL = "evolution.rdragentes.com.br"
    INSTANCE_ID = "PoupStress" 
    API_KEY = "62D811330286-4F48-B836-8FE1955A8A1F"

class ServerConfig:
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
```

### Delay entre Mensagens

Para evitar bloqueios do WhatsApp:
- **Padrão**: 1000ms (1 segundo)
- **Mínimo recomendado**: 500ms
- **Máximo**: 10000ms (10 segundos)

## 📝 Logs

O sistema gera logs detalhados:

```
INFO - Enviando mensagem para +5511999999999
INFO - Status da resposta: 200
INFO - Mensagem enviada para João Silva (+5511999999999): True
```

## 🚨 Troubleshooting

### Conexão com Evolution API falha
1. Verifique se a URL está correta
2. Confirme se a API key é válida
3. Teste a instância no painel Evolution

### Mensagens não são enviadas
1. Verifique se o WhatsApp está conectado
2. Confirme o formato do número de telefone
3. Verifique os logs do servidor

### Frontend não carrega
1. Confirme se o servidor está rodando na porta 8000
2. Verifique se não há conflitos de porta
3. Acesse http://localhost:8000 diretamente

## 🔒 Segurança

- Validação de entrada em todos os endpoints
- Sanitização de números de telefone
- Timeout de requisições configurado
- Logs de segurança habilitados

## 📈 Performance

- **Requests assíncronos** no frontend
- **Processamento em lote** eficiente
- **Cache de templates** habilitado
- **Compressão** de recursos estáticos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 💬 Suporte

Para suporte e dúvidas:
- Crie uma issue no GitHub
- Consulte a documentação da Evolution API: https://doc.evolution-api.com/

---

**WhatsApp Message Manager** - Sistema completo para gerenciamento de mensagens WhatsApp usando Evolution API v2. 