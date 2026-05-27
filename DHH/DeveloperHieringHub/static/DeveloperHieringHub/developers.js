// Font Management
function loadGoogleFonts() {
    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Roboto+Mono:wght@400;600&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);
}

loadGoogleFonts();

// Navbar Active Link Highlighting
function highlightActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'developers.html';
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href.includes(currentPage)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

highlightActiveNavLink();

// Logo Click Handler
const logo = document.querySelector('.logo');
if (logo) {
    logo.style.cursor = 'pointer';
    logo.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
}

// Navbar Icon Hover Effects
document.querySelectorAll('nav a').forEach(link => {
    const icon = link.querySelector('i');
    if (icon) {
        link.addEventListener('mouseenter', () => {
            icon.style.transform = 'rotate(10deg) scale(1.2)';
        });
        
        link.addEventListener('mouseleave', () => {
            icon.style.transform = 'rotate(0) scale(1)';
        });
    }
});

const cards = document.querySelectorAll(".developer-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {
        card.style.boxShadow = "0 0 30px rgba(0,128,128,0.25)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.boxShadow = "none";
    });

});