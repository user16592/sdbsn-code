// Ajouter ce script dans toutes vos pages
document.addEventListener('DOMContentLoaded', function() {
    // Correction des liens
    const currentPage = window.location.pathname.split('/').pop();
    
    // Si nous ne sommes pas sur la page d'accueil, ajuster les liens
    if (currentPage !== 'index.html' && currentPage !== '') {
        const links = document.querySelectorAll('a[href^="index.html"]');
        links.forEach(link => {
            if (link.getAttribute('href').startsWith('index.html#')) {
                const anchor = link.getAttribute('href').split('#')[1];
                link.setAttribute('href', `/#${anchor}`);
            } else {
                link.setAttribute('href', '/');
            }
        });
    }
    
    // Gestion du scroll pour les ancres
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            // Si nous sommes sur une page différente de l'accueil
            if (currentPage !== 'index.html' && currentPage !== '') {
                window.location.href = `/${targetId}`;
            } else {
                // Si nous sommes déjà sur l'accueil
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});