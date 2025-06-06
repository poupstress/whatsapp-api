<?php
/**
 * Exemplo de integração PHP com WhatsApp Message Manager
 * 
 * Este arquivo demonstra como usar o sistema Python a partir de um sistema PHP
 */

class WhatsAppMessageManager {
    private $baseUrl;
    
    public function __construct($baseUrl = 'http://localhost:8000') {
        $this->baseUrl = $baseUrl;
    }
    
    /**
     * Envia mensagem para um único contato
     */
    public function sendSingleMessage($name, $phone, $message) {
        $data = [
            'name' => $name,
            'phone' => $phone,
            'message' => $message
        ];
        
        $response = $this->makeRequest('/api/send-message', $data);
        return $response;
    }
    
    /**
     * Envia mensagens em massa para múltiplos contatos
     */
    public function sendBulkMessages($contacts, $message, $delay = 1000) {
        $data = [
            'contacts' => $contacts,
            'message' => $message,
            'delay' => $delay
        ];
        
        $response = $this->makeRequest('/api/send-bulk-messages', $data);
        return $response;
    }
    
    /**
     * Testa a conexão com o serviço
     */
    public function testConnection() {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->baseUrl . '/api/test-connection');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200) {
            return json_decode($response, true);
        } else {
            return ['success' => false, 'error' => 'HTTP ' . $httpCode];
        }
    }
    
    /**
     * Verifica o status do serviço
     */
    public function healthCheck() {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->baseUrl . '/api/health');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return $httpCode === 200;
    }
    
    /**
     * Método privado para fazer requisições HTTP
     */
    private function makeRequest($endpoint, $data) {
        $ch = curl_init();
        
        curl_setopt($ch, CURLOPT_URL, $this->baseUrl . $endpoint);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen(json_encode($data))
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            return [
                'success' => false,
                'error' => 'cURL Error: ' . $error
            ];
        }
        
        $decodedResponse = json_decode($response, true);
        
        if ($httpCode >= 200 && $httpCode < 300) {
            return $decodedResponse;
        } else {
            return [
                'success' => false,
                'error' => 'HTTP ' . $httpCode . ': ' . ($decodedResponse['detail'] ?? $response)
            ];
        }
    }
    
    /**
     * Formata número de telefone para o padrão brasileiro
     */
    public static function formatPhoneNumber($phone) {
        // Remove todos os caracteres não numéricos exceto +
        $cleanPhone = preg_replace('/[^\d+]/', '', $phone);
        
        // Adiciona +55 se não tiver código do país
        if (!str_starts_with($cleanPhone, '+')) {
            $cleanPhone = '+55' . $cleanPhone;
        }
        
        return $cleanPhone;
    }
    
    /**
     * Valida se o número de telefone está no formato correto
     */
    public static function validatePhoneNumber($phone) {
        $digitsOnly = preg_replace('/[^\d]/', '', $phone);
        return strlen($digitsOnly) >= 10 && strlen($digitsOnly) <= 15;
    }
}

// ==========================================
// EXEMPLOS DE USO
// ==========================================

try {
    $whatsapp = new WhatsAppMessageManager();
    
    // 1. Verificar se o serviço está funcionando
    echo "=== Verificando saúde do serviço ===\n";
    $isHealthy = $whatsapp->healthCheck();
    echo $isHealthy ? "✅ Serviço está funcionando\n" : "❌ Serviço não está respondendo\n";
    
    if (!$isHealthy) {
        exit("Erro: O serviço Python não está rodando. Execute 'python main.py' primeiro.\n");
    }
    
    // 2. Testar conexão com Evolution API
    echo "\n=== Testando conexão com Evolution API ===\n";
    $connectionTest = $whatsapp->testConnection();
    if ($connectionTest['success']) {
        echo "✅ Conexão com Evolution API OK\n";
    } else {
        echo "❌ Erro na conexão: " . $connectionTest['error'] . "\n";
    }
    
    // 3. Exemplo de mensagem individual
    echo "\n=== Enviando mensagem individual ===\n";
    $singleResult = $whatsapp->sendSingleMessage(
        'João da Silva',
        '+5511999999999',
        'Esta é uma mensagem de teste enviada via PHP!'
    );
    
    if ($singleResult['success']) {
        echo "✅ Mensagem individual enviada com sucesso!\n";
        echo "ID da mensagem: " . ($singleResult['message_id'] ?? 'N/A') . "\n";
    } else {
        echo "❌ Erro ao enviar mensagem individual: " . $singleResult['error'] . "\n";
    }
    
    // 4. Exemplo de mensagem em massa
    echo "\n=== Enviando mensagens em massa ===\n";
    
    $contacts = [
        ['name' => 'Maria Santos', 'phone' => '+5511888888888'],
        ['name' => 'Pedro Oliveira', 'phone' => '+5511777777777'],
        ['name' => 'Ana Costa', 'phone' => '+5511666666666']
    ];
    
    $bulkResult = $whatsapp->sendBulkMessages(
        $contacts,
        'Mensagem em massa enviada via integração PHP!',
        1500 // 1.5 segundos de delay
    );
    
    if ($bulkResult['success']) {
        echo "✅ Envio em massa concluído!\n";
        echo "Total de contatos: " . $bulkResult['total_contacts'] . "\n";
        echo "Sucessos: " . $bulkResult['successful_sends'] . "\n";
        echo "Falhas: " . $bulkResult['failed_sends'] . "\n";
        
        // Mostrar detalhes de cada envio
        echo "\n--- Detalhes dos envios ---\n";
        foreach ($bulkResult['results'] as $result) {
            $status = $result['success'] ? '✅' : '❌';
            $contact = array_values(array_filter($contacts, fn($c) => $c['phone'] === $result['sent_to']))[0] ?? null;
            $name = $contact ? $contact['name'] : 'N/A';
            
            echo "{$status} {$name} ({$result['sent_to']})";
            if (!$result['success']) {
                echo " - Erro: " . $result['error'];
            }
            echo "\n";
        }
    } else {
        echo "❌ Erro no envio em massa: " . $bulkResult['error'] . "\n";
    }
    
    // 5. Exemplo usando dados de um banco MySQL
    echo "\n=== Exemplo com banco de dados MySQL ===\n";
    
    /*
    // Descomente este bloco para usar com banco de dados real
    
    $pdo = new PDO('mysql:host=localhost;dbname=seu_banco', 'usuario', 'senha');
    
    $stmt = $pdo->prepare("SELECT nome, telefone FROM clientes WHERE ativo = 1");
    $stmt->execute();
    $clientes = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    $contactsFromDB = [];
    foreach ($clientes as $cliente) {
        $contactsFromDB[] = [
            'name' => $cliente['nome'],
            'phone' => WhatsAppMessageManager::formatPhoneNumber($cliente['telefone'])
        ];
    }
    
    $dbResult = $whatsapp->sendBulkMessages(
        $contactsFromDB,
        'Mensagem automática do sistema!'
    );
    
    echo "Mensagens enviadas para " . count($contactsFromDB) . " clientes do banco.\n";
    */
    
    echo "Exemplo simulado: Consultaria clientes no banco e enviaria mensagens.\n";
    
} catch (Exception $e) {
    echo "❌ Erro geral: " . $e->getMessage() . "\n";
}

// ==========================================
// FUNÇÃO HELPER PARA INTEGRAÇÃO EM OUTROS SISTEMAS
// ==========================================

/**
 * Função simples para envio rápido de mensagem
 * Pode ser chamada de qualquer lugar do seu sistema PHP
 */
function enviarWhatsApp($nome, $telefone, $mensagem) {
    $whatsapp = new WhatsAppMessageManager();
    return $whatsapp->sendSingleMessage($nome, $telefone, $mensagem);
}

/**
 * Função para envio em massa
 */
function enviarWhatsAppMassa($contatos, $mensagem, $delay = 1000) {
    $whatsapp = new WhatsAppMessageManager();
    return $whatsapp->sendBulkMessages($contatos, $mensagem, $delay);
}

// Exemplo de uso das funções helper:
// $resultado = enviarWhatsApp('João', '+5511999999999', 'Olá João!');
// echo $resultado['success'] ? 'Enviado!' : 'Erro: ' . $resultado['error'];

echo "\n=== Integração PHP concluída ===\n";
echo "Consulte o arquivo README.md para mais informações.\n";
?> 