// Font Management - Load Google Fonts dynamically
function loadGoogleFonts() {
    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Roboto+Mono:wght@400;600&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);
}

loadGoogleFonts();

// Navbar Active Link Highlighting
function highlightActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
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

// Falling Icons Animation
function createFallingIcons() {
    const container = document.querySelector('.falling-icons');
    if (!container) return;

    const icons = [
        { icon: 'fab fa-github', delay: 0 },
        { icon: 'fas fa-code', delay: 1 },
        { icon: 'fas fa-database', delay: 2 },
        { icon: 'fas fa-user-tie', delay: 0.5 },
        { icon: 'fab fa-google', delay: 1.5 },
        { icon: 'fas fa-laptop-code', delay: 2.5 },
        { icon: 'fas fa-cogs', delay: 0.8 },
        { icon: 'fas fa-brain', delay: 2.2 },
    ];

    // Create multiple falling icons
    for (let i = 0; i < 15; i++) {
        const icon = icons[i % icons.length];
        const fallingIcon = document.createElement('div');
        fallingIcon.className = 'falling-icon';
        fallingIcon.innerHTML = `<i class="${icon.icon}"></i>`;
        
        const randomLeft = Math.random() * 100;
        const randomDuration = 8 + Math.random() * 4;
        const randomDelay = Math.random() * 2;
        
        fallingIcon.style.left = randomLeft + '%';
        fallingIcon.style.animation = `fall ${randomDuration}s linear ${randomDelay}s infinite`;
        
        container.appendChild(fallingIcon);
    }
}

createFallingIcons();

// Logo Click Handler
const logo = document.querySelector('.logo');
if (logo) {
    logo.style.cursor = 'pointer';
    logo.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
}

// Smooth Scroll
document.documentElement.style.scrollBehavior = 'smooth';

// Button Interactions
const buttons = document.querySelectorAll('button');
buttons.forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-3px)';
        button.style.boxShadow = '0 10px 30px rgba(0, 128, 128, 0.4)';
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0)';
        button.style.boxShadow = 'none';
    });
});

// Navbar Icon Styling
const navIcons = document.querySelectorAll('nav a i');
navIcons.forEach(icon => {
    icon.style.marginRight = '6px';
    icon.style.transition = 'transform 0.3s ease';
});

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
