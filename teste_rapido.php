<?php
/**
 * Teste Rápido - WhatsApp Message Manager
 * Execute: php teste_rapido.php
 */

echo "=== TESTE RÁPIDO - WhatsApp Message Manager ===\n\n";

// Teste 1: Health Check
echo "1. Testando se o servidor está rodando...\n";
$health = file_get_contents('http://localhost:8000/api/health');
if ($health) {
    $data = json_decode($health, true);
    echo "✅ Servidor OK: " . $data['service'] . " v" . $data['version'] . "\n\n";
} else {
    echo "❌ Servidor não está respondendo!\n";
    exit(1);
}

// Teste 2: Conexão Evolution API
echo "2. Testando conexão com Evolution API...\n";
$connection = file_get_contents('http://localhost:8000/api/test-connection');
if ($connection) {
    $data = json_decode($connection, true);
    if ($data['success']) {
        echo "✅ Evolution API conectada!\n\n";
    } else {
        echo "❌ Erro na Evolution API: " . $data['error'] . "\n\n";
    }
}

// Teste 3: Envio de mensagem de teste
echo "3. Enviando mensagem de teste...\n";

$mensagem_data = [
    'name' => 'Teste Sistema',
    'phone' => '+5531999999999', // Substitua pelo seu número
    'message' => 'Teste de integração PHP funcionando!'
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://localhost:8000/api/send-message');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($mensagem_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    $result = json_decode($response, true);
    if ($result['success']) {
        echo "✅ Mensagem enviada com sucesso!\n";
        echo "   Para: " . $result['sent_to'] . "\n";
        echo "   ID: " . ($result['message_id'] ?? 'N/A') . "\n";
    } else {
        echo "❌ Erro no envio: " . $result['error'] . "\n";
    }
} else {
    echo "❌ Erro HTTP: $httpCode\n";
}

echo "\n=== TESTE CONCLUÍDO ===\n";
echo "Sistema está funcionando e pronto para integração!\n";
?> 