/**
 * Script principal pour l'application de gestion d'entreprise
 */

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Activer tous les tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Formater les montants en MAD
    formatMontants();
    
    // Ajouter des écouteurs d'événements pour les filtres
    setupFilters();
    
    // Initialiser les tableaux de données
    initDataTables();
});

/**
 * Formater les montants en MAD
 */
function formatMontants() {
    // Sélectionner tous les éléments avec la classe .format-mad
    document.querySelectorAll('.format-mad').forEach(function(element) {
        const montant = parseFloat(element.textContent);
        if (!isNaN(montant)) {
            element.textContent = formatMAD(montant);
        }
    });
}

/**
 * Formater un nombre en MAD
 * @param {number} montant - Le montant à formater
 * @returns {string} - Le montant formaté
 */
function formatMAD(montant) {
    return montant.toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }) + ' MAD';
}

/**
 * Configurer les filtres
 */
function setupFilters() {
    // Filtres pour les factures
    const filtresFactures = document.querySelectorAll('.filtre-facture');
    if (filtresFactures) {
        filtresFactures.forEach(function(filtre) {
            filtre.addEventListener('click', function(e) {
                e.preventDefault();
                const type = this.dataset.type;
                window.location.href = `/factures?type=${type}`;
            });
        });
    }
    
    // Filtres pour les projets
    const filtresProjets = document.querySelectorAll('.filtre-projet');
    if (filtresProjets) {
        filtresProjets.forEach(function(filtre) {
            filtre.addEventListener('click', function(e) {
                e.preventDefault();
                const etat = this.dataset.etat;
                window.location.href = `/projets?etat=${etat}`;
            });
        });
    }
}

/**
 * Initialiser les tableaux de données
 */
function initDataTables() {
    // Si DataTables est chargé et qu'il y a des tableaux à initialiser
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.datatable').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/French.json'
            },
            responsive: true,
            pageLength: 10
        });
    }
}

/**
 * Confirmer une action
 * @param {string} message - Le message de confirmation
 * @returns {boolean} - True si confirmé, false sinon
 */
function confirmerAction(message) {
    return confirm(message || 'Êtes-vous sûr de vouloir effectuer cette action ?');
}

/**
 * Afficher une notification
 * @param {string} message - Le message à afficher
 * @param {string} type - Le type de notification (success, danger, warning, info)
 */
function afficherNotification(message, type = 'info') {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.role = 'alert';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Ajouter au conteneur de notifications
    const container = document.getElementById('notifications-container') || document.body;
    container.appendChild(notification);
    
    // Supprimer après 5 secondes
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}