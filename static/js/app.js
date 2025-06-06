// WhatsApp Message Manager - Frontend JavaScript

class WhatsAppMessageManager {
    constructor() {
        this.contacts = [];
        this.init();
    }

    init() {
        // Bind event listeners
        this.bindEvents();
        
        // Test connection on load
        this.testConnection();
        
        console.log('WhatsApp Message Manager initialized');
    }

    bindEvents() {
        // Single message form
        document.getElementById('singleMessageForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendSingleMessage();
        });

        // Bulk message form
        document.getElementById('bulkMessageForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendBulkMessages();
        });

        // Add contact button
        document.getElementById('addContactBtn').addEventListener('click', () => {
            this.addContact();
        });

        // Test connection button
        document.getElementById('testConnectionBtn').addEventListener('click', () => {
            this.testConnection();
        });

        // Enter key on contact inputs
        ['contactName', 'contactPhone'].forEach(id => {
            document.getElementById(id).addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.addContact();
                }
            });
        });
    }

    // Utility functions
    showAlert(message, type = 'info', duration = 5000) {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" id="${alertId}" role="alert">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto dismiss
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, duration);
    }

    getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    showLoading(show = true) {
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        if (show) {
            loadingModal.show();
        } else {
            loadingModal.hide();
        }
    }

    formatPhoneNumber(phone) {
        // Remove all non-numeric characters except +
        let cleanPhone = phone.replace(/[^\d+]/g, '');
        
        // Add +55 if no country code
        if (!cleanPhone.startsWith('+')) {
            cleanPhone = '+55' + cleanPhone;
        }
        
        return cleanPhone;
    }

    validatePhoneNumber(phone) {
        const cleanPhone = phone.replace(/[^\d]/g, '');
        return cleanPhone.length >= 10 && cleanPhone.length <= 15;
    }

    // Connection testing
    async testConnection() {
        try {
            const response = await fetch('/api/test-connection');
            const result = await response.json();
            
            const statusContainer = document.getElementById('connectionStatus');
            
            if (result.success) {
                statusContainer.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-wifi connection-online me-2"></i>
                        <strong>Conexão Online</strong> - Evolution API está respondendo
                    </div>
                `;
                this.showAlert('Conexão com Evolution API estabelecida com sucesso!', 'success', 3000);
            } else {
                statusContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-wifi connection-offline me-2"></i>
                        <strong>Conexão Offline</strong> - Erro ao conectar com Evolution API
                        <br><small>${result.error || 'Erro desconhecido'}</small>
                    </div>
                `;
                this.showAlert('Erro ao conectar com Evolution API. Verifique as configurações.', 'danger');
            }
        } catch (error) {
            console.error('Error testing connection:', error);
            this.showAlert('Erro ao testar conexão: ' + error.message, 'danger');
        }
    }

    // Diagnóstico completo
    async runFullDiagnosis() {
        const diagnosticContainer = document.getElementById('diagnosticResults');
        
        // Mostrar loading
        diagnosticContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Executando diagnóstico...</span>
                </div>
                <p class="mt-2">Executando diagnóstico completo...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/full-diagnosis');
            const diagnosis = await response.json();
            
            let diagnosticHtml = `
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-stethoscope me-2"></i>Diagnóstico Completo</h5>
                        <small class="text-muted">Executado em: ${new Date(diagnosis.timestamp).toLocaleString('pt-BR')}</small>
                    </div>
                    <div class="card-body">
            `;

            // Resumo
            const summary = diagnosis.summary;
            diagnosticHtml += `
                <div class="row mb-3">
                    <div class="col-md-12">
                        <h6>Resumo do Sistema:</h6>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-server ${summary.api_reachable ? 'text-success' : 'text-danger'} me-2"></i>
                                    <span>API Evolution: ${summary.api_reachable ? 'Online' : 'Offline'}</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-cog ${summary.instance_found ? 'text-success' : 'text-danger'} me-2"></i>
                                    <span>Instância: ${summary.instance_found ? 'Encontrada' : 'Não encontrada'}</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="d-flex align-items-center">
                                    <i class="fab fa-whatsapp ${summary.whatsapp_connected ? 'text-success' : 'text-danger'} me-2"></i>
                                    <span>WhatsApp: ${summary.whatsapp_connected ? 'Conectado' : 'Desconectado'}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Issues
            if (summary.issues && summary.issues.length > 0) {
                diagnosticHtml += `
                    <div class="alert alert-warning">
                        <h6><i class="fas fa-exclamation-triangle me-2"></i>Problemas Identificados:</h6>
                        <ul class="mb-0">
                            ${summary.issues.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else {
                diagnosticHtml += `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>Nenhum problema identificado! Sistema funcionando normalmente.
                    </div>
                `;
            }

            // Detalhes da instância
            if (diagnosis.instance_status && diagnosis.instance_status.success) {
                const instance = diagnosis.instance_status;
                diagnosticHtml += `
                    <div class="card mt-3">
                        <div class="card-header">
                            <h6><i class="fas fa-info-circle me-2"></i>Detalhes da Instância</h6>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <strong>Nome:</strong> ${instance.instance_name || 'N/A'}<br>
                                    <strong>Status:</strong> 
                                    <span class="badge ${instance.is_connected ? 'bg-success' : 'bg-danger'}">
                                        ${instance.connection_status || 'Desconhecido'}
                                    </span><br>
                                    <strong>Telefone:</strong> ${instance.phone_number || 'N/A'}
                                </div>
                                <div class="col-md-6">
                                    <strong>Perfil:</strong> ${instance.profile_name || 'N/A'}<br>
                                    ${instance.profile_picture ? `<img src="${instance.profile_picture}" class="rounded-circle" width="50" height="50" alt="Profile">` : ''}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            diagnosticHtml += `
                    </div>
                </div>
            `;

            diagnosticContainer.innerHTML = diagnosticHtml;

            // Mostrar sugestões se houver problemas
            if (summary.issues && summary.issues.length > 0) {
                this.showAlert('Problemas identificados no diagnóstico. Verifique os detalhes abaixo.', 'warning', 5000);
            } else {
                this.showAlert('Diagnóstico concluído com sucesso!', 'success', 3000);
            }

        } catch (error) {
            console.error('Error running diagnosis:', error);
            diagnosticContainer.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Erro ao executar diagnóstico: ${error.message}
                </div>
            `;
            this.showAlert('Erro ao executar diagnóstico: ' + error.message, 'danger');
        }
    }

    // Listar instâncias disponíveis
    async listInstances() {
        const instancesContainer = document.getElementById('instancesList');
        
        // Mostrar loading
        instancesContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando instâncias...</span>
                </div>
                <p class="mt-2">Buscando instâncias disponíveis...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/list-instances');
            const result = await response.json();
            
            if (!result.success) {
                instancesContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        Erro ao buscar instâncias: ${result.error}
                    </div>
                `;
                return;
            }

            if (!result.instances || result.instances.length === 0) {
                instancesContainer.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Nenhuma instância encontrada.
                    </div>
                `;
                return;
            }

            // Exibir instâncias
            let instancesHtml = `
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-list me-2"></i>Instâncias Disponíveis (${result.total_instances})</h5>
                        <small class="text-muted">Instância atual configurada: <strong>${result.current_instance}</strong></small>
                    </div>
                    <div class="card-body">
                        <div class="row">
            `;

            result.instances.forEach((instance, index) => {
                const isCurrentInstance = instance.instance_name === result.current_instance;
                
                instancesHtml += `
                    <div class="col-md-6 mb-3">
                        <div class="card h-100 ${isCurrentInstance ? 'border-success' : ''}" style="cursor: pointer;" 
                             onclick="app.selectInstance('${instance.instance_name}')">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h6 class="card-title mb-0">
                                        ${instance.instance_name}
                                        ${isCurrentInstance ? '<span class="badge bg-success ms-2">ATUAL</span>' : ''}
                                    </h6>
                                    <span class="badge ${instance.is_connected ? 'bg-success' : 'bg-danger'}">
                                        ${instance.connection_status}
                                    </span>
                                </div>
                                
                                <div class="instance-details">
                                    <div class="d-flex align-items-center mb-2">
                                        ${instance.profile_picture ? 
                                            `<img src="${instance.profile_picture}" class="rounded-circle me-2" width="40" height="40" alt="Profile">` : 
                                            '<div class="bg-secondary rounded-circle me-2 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;"><i class="fas fa-user text-white"></i></div>'
                                        }
                                        <div>
                                            <div class="fw-bold">${instance.profile_name}</div>
                                            <small class="text-muted">${instance.phone_number}</small>
                                        </div>
                                    </div>
                                    
                                    <div class="mt-2">
                                        <small class="text-muted">
                                            <i class="fas fa-server me-1"></i>${instance.server_url}<br>
                                            <i class="fas fa-key me-1"></i>${instance.api_key}<br>
                                            <i class="fas fa-clock me-1"></i>Atualizado: ${new Date(instance.updated_at).toLocaleString('pt-BR')}
                                        </small>
                                    </div>
                                </div>
                            </div>
                            
                            ${isCurrentInstance ? '' : `
                                <div class="card-footer">
                                    <button type="button" class="btn btn-sm btn-outline-primary w-100" 
                                            onclick="app.selectInstance('${instance.instance_name}')">
                                        <i class="fas fa-check me-1"></i>Selecionar Instância
                                    </button>
                                </div>
                            `}
                        </div>
                    </div>
                `;
            });

            instancesHtml += `
                        </div>
                    </div>
                </div>
            `;

            instancesContainer.innerHTML = instancesHtml;
            this.showAlert(`${result.total_instances} instância(s) encontrada(s).`, 'success', 3000);

        } catch (error) {
            console.error('Error listing instances:', error);
            instancesContainer.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Erro ao buscar instâncias: ${error.message}
                </div>
            `;
            this.showAlert('Erro ao buscar instâncias: ' + error.message, 'danger');
        }
    }

    // Selecionar instância (apenas visual)
    selectInstance(instanceName) {
        this.showAlert(`Nota: A instância "${instanceName}" foi selecionada visualmente. Para alterar a configuração do backend, edite o arquivo config.py e reinicie o servidor.`, 'info', 8000);
        
        // Destacar instância selecionada visualmente
        document.querySelectorAll('.instance-card').forEach(card => {
            card.classList.remove('border-primary');
        });
        
        const selectedCard = document.querySelector(`[data-instance="${instanceName}"]`);
        if (selectedCard) {
            selectedCard.classList.add('border-primary');
        }
    }

    // Single message functionality
    async sendSingleMessage() {
        const name = document.getElementById('singleName').value.trim();
        const phone = document.getElementById('singlePhone').value.trim();
        const message = document.getElementById('singleMessage').value.trim();

        if (!name || !phone || !message) {
            this.showAlert('Por favor, preencha todos os campos obrigatórios.', 'warning');
            return;
        }

        const formattedPhone = this.formatPhoneNumber(phone);
        if (!this.validatePhoneNumber(formattedPhone)) {
            this.showAlert('Número de telefone inválido. Use o formato: +5511999999999', 'danger');
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch('/api/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    phone: formattedPhone,
                    message: message
                })
            });

            const result = await response.json();
            
            this.showLoading(false);

            if (response.ok && result.success) {
                this.showAlert(`Mensagem enviada com sucesso para ${name}!`, 'success');
                
                // Clear form
                document.getElementById('singleMessageForm').reset();
                
                // Show result
                this.showSingleResult(result, name, formattedPhone);
            } else {
                this.showAlert(`Erro ao enviar mensagem: ${result.error || 'Erro desconhecido'}`, 'danger');
                this.showSingleResult(result, name, formattedPhone);
            }
        } catch (error) {
            this.showLoading(false);
            console.error('Error sending single message:', error);
            this.showAlert('Erro ao enviar mensagem: ' + error.message, 'danger');
        }
    }

    showSingleResult(result, name, phone) {
        const resultsContainer = document.getElementById('resultsContainer');
        const isSuccess = result.success;
        
        const resultHtml = `
            <div class="card result-item ${isSuccess ? 'result-success' : 'result-error'} fade-in">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-${isSuccess ? 'check-circle text-success' : 'times-circle text-danger'} me-3 fs-4"></i>
                        <div class="flex-grow-1">
                            <h6 class="mb-1">${name} (${phone})</h6>
                            <p class="mb-0 text-muted">
                                ${isSuccess ? 'Mensagem enviada com sucesso' : `Erro: ${result.error}`}
                            </p>
                            ${result.message_id ? `<small class="text-muted">ID: ${result.message_id}</small>` : ''}
                        </div>
                        <small class="text-muted">${new Date().toLocaleString('pt-BR')}</small>
                    </div>
                </div>
            </div>
        `;
        
        resultsContainer.insertAdjacentHTML('afterbegin', resultHtml);
    }

    // Contact management
    addContact() {
        const nameInput = document.getElementById('contactName');
        const phoneInput = document.getElementById('contactPhone');
        
        const name = nameInput.value.trim();
        const phone = phoneInput.value.trim();

        if (!name || !phone) {
            this.showAlert('Por favor, preencha o nome e telefone do contato.', 'warning');
            return;
        }

        const formattedPhone = this.formatPhoneNumber(phone);
        if (!this.validatePhoneNumber(formattedPhone)) {
            this.showAlert('Número de telefone inválido. Use o formato: +5511999999999', 'danger');
            return;
        }

        // Check if contact already exists
        const existingContact = this.contacts.find(c => c.phone === formattedPhone);
        if (existingContact) {
            this.showAlert('Este número já está na lista de contatos.', 'warning');
            return;
        }

        // Add contact
        const contact = {
            id: Date.now(),
            name: name,
            phone: formattedPhone
        };

        this.contacts.push(contact);
        this.updateContactsList();
        
        // Clear inputs
        nameInput.value = '';
        phoneInput.value = '';
        nameInput.focus();

        this.showAlert(`Contato ${name} adicionado com sucesso!`, 'success', 2000);
    }

    removeContact(contactId) {
        this.contacts = this.contacts.filter(c => c.id !== contactId);
        this.updateContactsList();
        this.showAlert('Contato removido com sucesso!', 'info', 2000);
    }

    updateContactsList() {
        const contactsList = document.getElementById('contactsList');
        const contactCount = document.getElementById('contactCount');
        
        contactCount.textContent = this.contacts.length;

        if (this.contacts.length === 0) {
            contactsList.innerHTML = '<p class="text-muted mb-0">Nenhum contato adicionado ainda.</p>';
            return;
        }

        const contactsHtml = this.contacts.map(contact => `
            <div class="contact-item d-flex justify-content-between align-items-center">
                <div>
                    <div class="contact-name">${contact.name}</div>
                    <div class="contact-phone">${contact.phone}</div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="app.removeContact(${contact.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');

        contactsList.innerHTML = contactsHtml;
    }

    // Bulk message functionality
    async sendBulkMessages() {
        const message = document.getElementById('bulkMessage').value.trim();
        const delay = parseInt(document.getElementById('messageDelay').value) || 1000;

        if (!message) {
            this.showAlert('Por favor, digite a mensagem.', 'warning');
            return;
        }

        if (this.contacts.length === 0) {
            this.showAlert('Adicione pelo menos um contato antes de enviar.', 'warning');
            return;
        }

        try {
            this.showLoading(true);
            
            const response = await fetch('/api/send-bulk-messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contacts: this.contacts,
                    message: message,
                    delay: delay
                })
            });

            const result = await response.json();
            
            this.showLoading(false);

            if (response.ok && result.success) {
                this.showAlert(`Envio em massa concluído! ${result.successful_sends} enviadas, ${result.failed_sends} falharam.`, 'success');
                
                // Show detailed results
                this.showBulkResults(result.results);
                
                // Clear form
                document.getElementById('bulkMessage').value = '';
                
            } else {
                this.showAlert(`Erro no envio em massa: ${result.detail || 'Erro desconhecido'}`, 'danger');
            }
        } catch (error) {
            this.showLoading(false);
            console.error('Error sending bulk messages:', error);
            this.showAlert('Erro ao enviar mensagens em massa: ' + error.message, 'danger');
        }
    }

    showBulkResults(results) {
        const resultsContainer = document.getElementById('resultsContainer');
        
        // Summary card
        const successful = results.filter(r => r.success).length;
        const failed = results.length - successful;
        
        const summaryHtml = `
            <div class="card mb-3 fade-in">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-chart-bar me-2"></i>
                        Resultado do Envio em Massa
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-md-4">
                            <div class="border rounded p-3">
                                <h3 class="text-primary mb-1">${results.length}</h3>
                                <small class="text-muted">Total</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="border rounded p-3">
                                <h3 class="text-success mb-1">${successful}</h3>
                                <small class="text-muted">Sucessos</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="border rounded p-3">
                                <h3 class="text-danger mb-1">${failed}</h3>
                                <small class="text-muted">Falhas</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Detailed results
        const detailedResultsHtml = results.map(result => {
            const isSuccess = result.success;
            const contact = this.contacts.find(c => c.phone === result.sent_to);
            
            return `
                <div class="card result-item ${isSuccess ? 'result-success' : 'result-error'} fade-in mb-2">
                    <div class="card-body py-2">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-${isSuccess ? 'check-circle text-success' : 'times-circle text-danger'} me-3"></i>
                            <div class="flex-grow-1">
                                <strong>${contact ? contact.name : 'N/A'}</strong>
                                <span class="text-muted"> - ${result.sent_to}</span>
                                ${!isSuccess ? `<br><small class="text-danger">${result.error}</small>` : ''}
                            </div>
                            <small class="text-muted">${new Date().toLocaleString('pt-BR')}</small>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        resultsContainer.innerHTML = summaryHtml + detailedResultsHtml;
    }
}

// Initialize the application
const app = new WhatsAppMessageManager();

// Expose app globally for inline event handlers
window.app = app; 