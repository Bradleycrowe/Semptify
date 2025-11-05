// Semptify SPA - JavaScript Navigation and Interactions

document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initQuickActions();
    initVaultButton();
});

// Navigation System
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const pages = document.querySelectorAll('.page');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetPage = this.getAttribute('data-page');
            
            // Update active nav button
            navButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show target page
            pages.forEach(page => {
                if (page.id === `page-${targetPage}`) {
                    page.classList.add('active');
                } else {
                    page.classList.remove('active');
                }
            });
            
            // Update URL hash without scrolling
            history.pushState(null, '', `#${targetPage}`);
        });
    });
    
    // Handle browser back/forward
    window.addEventListener('popstate', function() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            const btn = document.querySelector(`.nav-btn[data-page="${hash}"]`);
            if (btn) {
                btn.click();
            }
        }
    });
    
    // Handle initial hash on page load
    const initialHash = window.location.hash.slice(1);
    if (initialHash) {
        const btn = document.querySelector(`.nav-btn[data-page="${initialHash}"]`);
        if (btn) {
            btn.click();
        }
    }
}

// Quick Action Cards
function initQuickActions() {
    const actionCards = document.querySelectorAll('.action-card[data-modal]');
    
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const modalType = this.getAttribute('data-modal');
            openModal(modalType);
        });
    });
}

// Vault Button
function initVaultButton() {
    const vaultBtn = document.getElementById('btn-vault');
    if (vaultBtn) {
        vaultBtn.addEventListener('click', function() {
            window.location.href = '/vault';
        });
    }
    
    const settingsBtn = document.getElementById('btn-settings');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', function() {
            window.location.href = '/admin';
        });
    }
    
    const helpBtn = document.getElementById('btn-help');
    if (helpBtn) {
        helpBtn.addEventListener('click', function() {
            alert('Help & Documentation\n\nFor help, visit the Library section or contact support.');
        });
    }
}

// Modal System (placeholder - can be expanded)
function openModal(modalType) {
    console.log('Opening modal:', modalType);
    
    // Map modal types to actual routes
    const modalRoutes = {
        'witness-form': '/witness',
        'evidence-packet': '/packet',
        'complaint': '/modules/law_notes/complaint_templates',
        'notary': '/notary',
        'court-file': '/court-filing',
        'service-animal': '/service-animal',
        'statute': '/statute-calculator',
        'rights': '/rights-explorer'
    };
    
    const route = modalRoutes[modalType];
    if (route) {
        window.location.href = route;
    } else {
        alert(`Feature coming soon: ${modalType}`);
    }
}

// Dynamic Stats Update (can be connected to API later)
function updateStats() {
    // Placeholder for future API integration
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update stat numbers dynamically
            console.log('Stats:', data);
        })
        .catch(error => {
            console.log('Stats not yet available');
        });
}

// Call on page load
setTimeout(updateStats, 1000);
