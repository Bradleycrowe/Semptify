/* ============================================================================
   SEMPTIFY SPA - MODAL & INTERACTION SYSTEM
   ============================================================================ */

class ModalSystem {
    constructor() {
        this.modals = new Map();
        this.activeModals = [];
        this.overlay = document.getElementById('modal-overlay');
        this.container = document.getElementById('modals-container');
        this.init();
    }

    init() {
        this.overlay.addEventListener('click', () => this.closeTopModal());
        this.setupModals();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Page navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.navigatePage(e.target.closest('.nav-btn').dataset.page));
        });

        // Modal triggers
        document.querySelectorAll('[data-modal]').forEach(btn => {
            btn.addEventListener('click', () => {
                const modalId = btn.dataset.modal;
                this.open(modalId);
            });
        });

        // Sidebar buttons
        document.getElementById('btn-vault')?.addEventListener('click', () => this.open('vault'));
        document.getElementById('btn-settings')?.addEventListener('click', () => this.open('settings'));
        document.getElementById('btn-help')?.addEventListener('click', () => this.open('help'));
    }

    setupModals() {
        const modals = [
            this.createWitnessModal(),
            this.createEvidencePacketModal(),
            this.createComplaintModal(),
            this.createNotaryModal(),
            this.createCourtFileModal(),
            this.createServiceAnimalModal(),
            this.createStatuteModal(),
            this.createRightsModal(),
            this.createVaultModal(),
            this.createSettingsModal(),
            this.createHelpModal()
        ];

        modals.forEach(modal => {
            if (modal) {
                this.modals.set(modal.id, modal);
                this.container.appendChild(modal);
            }
        });
    }

    createWitnessModal() {
        return this.createModal('witness-form', 'Witness Statement', `
            <form id="form-witness">
                <div class="form-group">
                    <label for="witness-name">Witness Name *</label>
                    <input type="text" id="witness-name" name="witness_name" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="witness-date">Date of Incident *</label>
                        <input type="date" id="witness-date" name="incident_date" required>
                    </div>
                    <div class="form-group">
                        <label for="witness-location">Location *</label>
                        <input type="text" id="witness-location" name="location" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="witness-statement">Witness Statement *</label>
                    <textarea id="witness-statement" name="statement" required placeholder="Provide detailed account of what you witnessed..."></textarea>
                </div>
                <div class="form-group">
                    <label for="witness-email">Contact Email</label>
                    <input type="email" id="witness-email" name="email">
                </div>
                <div class="form-group">
                    <label for="witness-phone">Contact Phone</label>
                    <input type="tel" id="witness-phone" name="phone">
                </div>
            </form>
        `, ['Submit Statement', 'Cancel']);
    }

    createEvidencePacketModal() {
        return this.createModal('evidence-packet', 'Evidence Packet Builder', `
            <form id="form-evidence">
                <div class="form-group">
                    <label for="packet-title">Packet Title *</label>
                    <input type="text" id="packet-title" name="title" required>
                </div>
                <div class="form-group">
                    <label for="packet-description">Description *</label>
                    <textarea id="packet-description" name="description" required placeholder="Describe the evidence and its relevance..."></textarea>
                </div>
                <div class="form-group">
                    <label for="packet-files">Upload Files *</label>
                    <input type="file" id="packet-files" name="files" multiple required accept="image/*,video/*,audio/*,application/pdf,.doc,.docx">
                </div>
                <div class="form-group">
                    <label for="packet-type">Evidence Type *</label>
                    <select id="packet-type" name="type" required>
                        <option value="">Select...</option>
                        <option value="photos">Photos/Images</option>
                        <option value="videos">Videos</option>
                        <option value="audio">Audio Recordings</option>
                        <option value="documents">Documents</option>
                        <option value="communications">Communications</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="packet-chain">Chain of Custody</label>
                    <textarea id="packet-chain" name="chain_of_custody" placeholder="Document how evidence was handled..."></textarea>
                </div>
            </form>
        `, ['Create Packet', 'Cancel']);
    }

    createComplaintModal() {
        return this.createModal('complaint', 'Generate Complaint', `
            <form id="form-complaint">
                <div class="form-group">
                    <label for="complaint-plaintiff">Plaintiff Name *</label>
                    <input type="text" id="complaint-plaintiff" name="plaintiff" required>
                </div>
                <div class="form-group">
                    <label for="complaint-defendant">Defendant Name *</label>
                    <input type="text" id="complaint-defendant" name="defendant" required>
                </div>
                <div class="form-group">
                    <label for="complaint-jurisdiction">Jurisdiction *</label>
                    <select id="complaint-jurisdiction" name="jurisdiction" required>
                        <option value="">Select...</option>
                        <option value="federal">Federal Court</option>
                        <option value="state">State Court</option>
                        <option value="county">County Court</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="complaint-type">Complaint Type *</label>
                    <select id="complaint-type" name="type" required>
                        <option value="">Select...</option>
                        <option value="housing">Housing/Landlord</option>
                        <option value="employment">Employment</option>
                        <option value="contract">Contract Dispute</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="complaint-facts">Facts of the Case *</label>
                    <textarea id="complaint-facts" name="facts" required placeholder="Describe the facts and circumstances..."></textarea>
                </div>
                <div class="form-group">
                    <label for="complaint-relief">Relief Sought *</label>
                    <textarea id="complaint-relief" name="relief" required placeholder="What remedy are you seeking?"></textarea>
                </div>
            </form>
        `, ['Generate Document', 'Cancel']);
    }

    createNotaryModal() {
        return this.createModal('notary', 'Virtual Notary (RON)', `
            <div style="padding: var(--space-lg);">
                <p style="margin-bottom: var(--space-lg); color: var(--text-secondary);">
                    Get your documents notarized through Remote Online Notarization (RON). A licensed notary will verify your identity and authenticate your documents.
                </p>
                <form id="form-notary">
                    <div class="form-group">
                        <label for="notary-document">Upload Document *</label>
                        <input type="file" id="notary-document" name="document" required accept="application/pdf,.doc,.docx,image/*">
                    </div>
                    <div class="form-group">
                        <label for="notary-fullname">Full Name *</label>
                        <input type="text" id="notary-fullname" name="fullname" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="notary-state">State *</label>
                            <select id="notary-state" name="state" required>
                                <option value="">Select...</option>
                                <option value="CA">California</option>
                                <option value="NY">New York</option>
                                <option value="TX">Texas</option>
                                <option value="MN">Minnesota</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="notary-id">ID Type *</label>
                            <select id="notary-id" name="id_type" required>
                                <option value="">Select...</option>
                                <option value="drivers-license">Driver's License</option>
                                <option value="passport">Passport</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="notary-phone">Phone Number *</label>
                        <input type="tel" id="notary-phone" name="phone" required>
                    </div>
                </form>
                <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: var(--space-lg);">
                    💡 <strong>Tip:</strong> Have your ID ready for video verification. The process takes about 10-15 minutes.
                </p>
            </div>
        `, ['Start Notarization', 'Cancel']);
    }

    createCourtFileModal() {
        return this.createModal('court-file', 'Court Filing', `
            <form id="form-court">
                <div class="form-group">
                    <label for="court-name">Court Name *</label>
                    <input type="text" id="court-name" name="court_name" required>
                </div>
                <div class="form-group">
                    <label for="court-case">Case Number *</label>
                    <input type="text" id="court-case" name="case_number" required>
                </div>
                <div class="form-group">
                    <label for="court-type">Filing Type *</label>
                    <select id="court-type" name="filing_type" required>
                        <option value="">Select...</option>
                        <option value="complaint">Complaint</option>
                        <option value="motion">Motion</option>
                        <option value="response">Response</option>
                        <option value="brief">Brief</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="court-method">Submission Method *</label>
                    <select id="court-method" name="submission_method" required>
                        <option value="">Select...</option>
                        <option value="ecf">Electronic Court Filing (ECF)</option>
                        <option value="email">Email</option>
                        <option value="mail">Certified Mail</option>
                        <option value="hand">Hand Delivery</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="court-documents">Attach Documents *</label>
                    <input type="file" id="court-documents" name="documents" multiple required accept="application/pdf,.doc,.docx">
                </div>
            </form>
        `, ['Submit Filing', 'Cancel']);
    }

    createServiceAnimalModal() {
        return this.createModal('service-animal', 'Service Animal Documentation', `
            <form id="form-service-animal">
                <div class="form-group">
                    <label for="sa-animal-type">Animal Type *</label>
                    <select id="sa-animal-type" name="animal_type" required>
                        <option value="">Select...</option>
                        <option value="dog">Dog</option>
                        <option value="cat">Cat</option>
                        <option value="miniature-horse">Miniature Horse</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="sa-animal-name">Animal Name *</label>
                    <input type="text" id="sa-animal-name" name="animal_name" required>
                </div>
                <div class="form-group">
                    <label for="sa-service">Service Provided *</label>
                    <textarea id="sa-service" name="service" required placeholder="Describe the service the animal provides..."></textarea>
                </div>
                <div class="form-group">
                    <label for="sa-disability">Related Disability *</label>
                    <textarea id="sa-disability" name="disability" required placeholder="Explain the disability and how the animal assists..."></textarea>
                </div>
                <div class="form-group">
                    <label for="sa-training">Training Certification</label>
                    <input type="file" id="sa-training" name="training_cert" accept="application/pdf,.doc,.docx,image/*">
                </div>
            </form>
        `, ['Submit Documentation', 'Cancel']);
    }

    createStatuteModal() {
        return this.createModal('statute', 'Statute Calculator', `
            <div style="padding: var(--space-lg);">
                <form id="form-statute">
                    <div class="form-group">
                        <label for="statute-type">Claim Type *</label>
                        <select id="statute-type" name="claim_type" required>
                            <option value="">Select...</option>
                            <option value="housing">Housing Violation</option>
                            <option value="employment">Employment Discrimination</option>
                            <option value="contract">Contract Breach</option>
                            <option value="injury">Personal Injury</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="statute-state">State/Jurisdiction *</label>
                        <select id="statute-state" name="state" required>
                            <option value="">Select...</option>
                            <option value="MN">Minnesota</option>
                            <option value="CA">California</option>
                            <option value="NY">New York</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="statute-date">Date of Event *</label>
                        <input type="date" id="statute-date" name="event_date" required>
                    </div>
                </form>
                <div id="statute-result" style="display:none; margin-top: var(--space-lg); padding: var(--space-lg); background: var(--lighter); border-radius: var(--radius-md); border-left: 4px solid var(--secondary);">
                    <h4>Deadline Calculation</h4>
                    <p id="statute-text"></p>
                </div>
            </div>
        `, ['Calculate', 'Cancel']);
    }

    createRightsModal() {
        return this.createModal('rights', 'Know Your Rights', `
            <div style="padding: var(--space-lg);">
                <p style="margin-bottom: var(--space-lg); color: var(--text-secondary);">
                    Select a category to learn about your rights:
                </p>
                <div style="display: grid; grid-template-columns: 1fr; gap: var(--space-md);">
                    <button style="padding: var(--space-md); border: 2px solid var(--light); border-radius: var(--radius-md); background: white; cursor: pointer; text-align: left; transition: all var(--transition-normal);" onmouseover="this.style.borderColor='var(--secondary)'; this.style.backgroundColor='var(--lighter)'" onmouseout="this.style.borderColor='var(--light)'; this.style.backgroundColor='white'">
                        <h4 style="margin: 0 0 0.5rem 0;">🏠 Housing Rights</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Tenant rights, lease agreements, eviction procedures</p>
                    </button>
                    <button style="padding: var(--space-md); border: 2px solid var(--light); border-radius: var(--radius-md); background: white; cursor: pointer; text-align: left; transition: all var(--transition-normal);" onmouseover="this.style.borderColor='var(--secondary)'; this.style.backgroundColor='var(--lighter)'" onmouseout="this.style.borderColor='var(--light)'; this.style.backgroundColor='white'">
                        <h4 style="margin: 0 0 0.5rem 0;">💼 Employment Rights</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Discrimination, harassment, wrongful termination</p>
                    </button>
                    <button style="padding: var(--space-md); border: 2px solid var(--light); border-radius: var(--radius-md); background: white; cursor: pointer; text-align: left; transition: all var(--transition-normal);" onmouseover="this.style.borderColor='var(--secondary)'; this.style.backgroundColor='var(--lighter)'" onmouseout="this.style.borderColor='var(--light)'; this.style.backgroundColor='white'">
                        <h4 style="margin: 0 0 0.5rem 0;">♿ Disability Rights</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">ADA accommodations, accessibility, service animals</p>
                    </button>
                    <button style="padding: var(--space-md); border: 2px solid var(--light); border-radius: var(--radius-md); background: white; cursor: pointer; text-align: left; transition: all var(--transition-normal);" onmouseover="this.style.borderColor='var(--secondary)'; this.style.backgroundColor='var(--lighter)'" onmouseout="this.style.borderColor='var(--light)'; this.style.backgroundColor='white'">
                        <h4 style="margin: 0 0 0.5rem 0;">👨‍⚖️ Due Process</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Court procedures, legal representation, appeals</p>
                    </button>
                </div>
            </div>
        `, ['Close']);
    }

    createVaultModal() {
        return this.createModal('vault', 'Document Vault', `
            <div style="padding: var(--space-lg);">
                <p style="margin-bottom: var(--space-lg); color: var(--text-secondary);">
                    Securely store and manage your important documents, evidence, and communications.
                </p>
                <div style="display: grid; gap: var(--space-md);">
                    <button style="padding: var(--space-lg); border: 2px dashed var(--secondary); border-radius: var(--radius-md); background: transparent; cursor: pointer;">
                        <i class="fas fa-cloud-upload-alt" style="font-size: 2rem; color: var(--secondary); margin-bottom: var(--space-md); display: block;"></i>
                        <p style="margin: 0; font-weight: 600; color: var(--primary);">Upload Documents</p>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Drag and drop or click to browse</p>
                    </button>
                    <div style="border-top: 1px solid var(--light); padding-top: var(--space-lg);">
                        <h4 style="margin-bottom: var(--space-md);">Recent Files</h4>
                        <p style="color: var(--text-secondary); text-align: center;">No files yet</p>
                    </div>
                </div>
            </div>
        `, ['Close']);
    }

    createSettingsModal() {
        return this.createModal('settings', 'Settings', `
            <form id="form-settings">
                <div class="form-group">
                    <label for="settings-name">Full Name</label>
                    <input type="text" id="settings-name" name="name">
                </div>
                <div class="form-group">
                    <label for="settings-email">Email</label>
                    <input type="email" id="settings-email" name="email">
                </div>
                <div class="form-group">
                    <label for="settings-phone">Phone</label>
                    <input type="tel" id="settings-phone" name="phone">
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="settings-notifications" name="notifications" checked>
                        Email Notifications
                    </label>
                </div>
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="settings-analytics" name="analytics" checked>
                        Allow Analytics
                    </label>
                </div>
            </form>
        `, ['Save Settings', 'Cancel']);
    }

    createHelpModal() {
        return this.createModal('help', 'Help & Support', `
            <div style="padding: var(--space-lg);">
                <div style="display: grid; gap: var(--space-lg);">
                    <div>
                        <h4 style="margin-bottom: var(--space-md); color: var(--primary);">❓ Frequently Asked Questions</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 0;">Find answers to common questions about using Semptify.</p>
                    </div>
                    <div>
                        <h4 style="margin-bottom: var(--space-md); color: var(--primary);">📖 Getting Started Guide</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 0;">Step-by-step guide to get started with Semptify.</p>
                    </div>
                    <div>
                        <h4 style="margin-bottom: var(--space-md); color: var(--primary);">💬 Contact Support</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 0;">Email: support@semptify.com | Phone: 1-800-SEMPTIFY</p>
                    </div>
                    <div>
                        <h4 style="margin-bottom: var(--space-md); color: var(--primary);">🔒 Privacy & Security</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 0;">Learn about how we protect your data and privacy.</p>
                    </div>
                </div>
            </div>
        `, ['Close']);
    }

    createModal(id, title, content, actions) {
        const modal = document.createElement('div');
        modal.id = id;
        modal.className = 'modal';

        const buttonsHtml = actions.map((action, i) => {
            const btnClass = i === 0 ? 'btn btn-primary' : 'btn btn-outline';
            return `<button type="button" class="${btnClass}">${action}</button>`;
        }).join('');

        modal.innerHTML = `
            <div class="modal-header">
                <h2>${title}</h2>
                <button type="button" class="modal-close" data-close>&times;</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            <div class="modal-footer">
                ${buttonsHtml}
            </div>
        `;

        // Close button
        modal.querySelector('[data-close]').addEventListener('click', () => this.close(id));

        // Action buttons
        const buttons = modal.querySelectorAll('.modal-footer button');
        buttons.forEach((btn, i) => {
            btn.addEventListener('click', (e) => {
                if (actions[i].toLowerCase().includes('cancel') || actions[i].toLowerCase() === 'close') {
                    this.close(id);
                } else {
                    this.handleSubmit(id, e);
                }
            });
        });

        return modal;
    }

    navigatePage(page) {
        // Update nav buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.page === page);
        });

        // Update pages
        document.querySelectorAll('.page').forEach(p => {
            p.classList.remove('active');
        });
        document.getElementById(`page-${page}`).classList.add('active');
    }

    open(id) {
        const modal = this.modals.get(id);
        if (!modal) return;

        modal.classList.add('active');
        this.activeModals.push(id);
        this.overlay.classList.add('active');
    }

    closeTopModal() {
        if (this.activeModals.length > 0) {
            this.close(this.activeModals[this.activeModals.length - 1]);
        }
    }

    close(id) {
        const modal = this.modals.get(id);
        if (!modal) return;

        modal.classList.remove('active');
        this.activeModals = this.activeModals.filter(m => m !== id);

        if (this.activeModals.length === 0) {
            this.overlay.classList.remove('active');
        }
    }

    async handleSubmit(id, event) {
        event.preventDefault();
        const modal = this.modals.get(id);
        const form = modal.querySelector('form');

        if (form) {
            const formData = new FormData(form);

            // Add CSRF token if available
            const csrfToken = document.querySelector('input[name="csrf_token"]')?.value ||
                             localStorage.getItem('csrf_token');
            if (csrfToken) {
                formData.append('csrf_token', csrfToken);
            }

            // Map modal ID to endpoint
            const endpoints = {
                'witness-form': '/witness_statement_save',
                'evidence-packet': '/api/evidence/packet/create',
                'complaint': '/api/complaint/generate',
                'notary': '/legal_notary',
                'court-file': '/court_clerk',
                'service-animal': '/api/service-animal/create',
                'statute': '/api/statute/calculate'
            };

            const endpoint = endpoints[id] || '/api/submit';

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Request-Id': this.generateRequestId()
                    }
                });

                if (response.ok) {
                    const data = await response.json().catch(() => ({}));
                    console.log(`✅ ${id} submitted successfully:`, data);

                    // Show success notification
                    this.showNotification(`${this.humanize(id)} submitted successfully!`, 'success');
                    this.close(id);

                    // Refresh relevant page
                    this.refreshPage();
                } else {
                    console.error(`❌ Error submitting ${id}:`, response.status);
                    this.showNotification(`Error submitting form. Please try again.`, 'error');
                }
            } catch (error) {
                console.error(`Error submitting ${id}:`, error);
                this.showNotification(`Network error. Please check your connection.`, 'error');
            }
        } else {
            this.close(id);
        }
    }

    generateRequestId() {
        return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    humanize(str) {
        return str
            .replace(/-/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 3000;
            animation: slideIn 300ms ease-out;
            font-weight: 500;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 300ms ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    refreshPage() {
        // Refresh current page data if needed
        const activePage = document.querySelector('.page.active').id.replace('page-', '');
        // Could trigger data refresh here based on page type
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.modalSystem = new ModalSystem();
});
