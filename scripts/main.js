/* ============================================
   DHH — Developers Hiring Hub
   Main JavaScript
   Built by Quick Red Tech Software Development Studio
   ============================================ */

// ============================================
// FIREBASE CONFIGURATION (Placeholder - Replace with your actual config)
// ============================================
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "your-app.firebaseapp.com",
    projectId: "your-app",
    storageBucket: "your-app.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};

// Initialize Firebase (commented out until you add real config)
// firebase.initializeApp(firebaseConfig);
// const auth = firebase.auth();

// ============================================
// THREE.JS HERO BACKGROUND ANIMATION
// ============================================
class HeroBackground {
    constructor() {
        this.canvas = document.getElementById('three-canvas');
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, alpha: true, antialias: true });
        
        this.particles = null;
        this.grid = null;
        this.spheres = [];
        
        this.mouseX = 0;
        this.mouseY = 0;
        
        this.init();
        this.animate();
        this.handleResize();
    }
    
    init() {
        // Set renderer properties
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Position camera
        this.camera.position.z = 50;
        
        // Create particles
        this.createParticles();
        
        // Create grid floor
        this.createGrid();
        
        // Create floating spheres
        this.createSpheres();
        
        // Add lights
        this.addLights();
        
        // Event listeners
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
    }
    
    createParticles() {
        const particleCount = 2000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        const color = new THREE.Color('#00f5d4');
        
        for (let i = 0; i < particleCount * 3; i += 3) {
            // Positions
            positions[i] = (Math.random() - 0.5) * 200;
            positions[i + 1] = (Math.random() - 0.5) * 200;
            positions[i + 2] = (Math.random() - 0.5) * 200;
            
            // Colors with variation
            const variance = Math.random() * 0.3;
            colors[i] = color.r + variance * 0.2;
            colors[i + 1] = color.g + variance * 0.2;
            colors[i + 2] = color.b + variance * 0.2;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 0.5,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });
        
        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);
    }
    
    createGrid() {
        const gridSize = 200;
        const gridDivisions = 50;
        
        const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, '#00f5d4', '#1a1a1a');
        gridHelper.position.y = -30;
        gridHelper.rotation.x = Math.PI / 4;
        
        this.grid = gridHelper;
        this.scene.add(this.grid);
    }
    
    createSpheres() {
        const sphereGeometry = new THREE.SphereGeometry(2, 32, 32);
        const sphereMaterial = new THREE.MeshPhongMaterial({
            color: 0x00f5d4,
            emissive: 0x004444,
            specular: 0xffffff,
            shininess: 100,
            transparent: true,
            opacity: 0.8
        });
        
        for (let i = 0; i < 5; i++) {
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial.clone());
            sphere.position.set(
                (Math.random() - 0.5) * 80,
                (Math.random() - 0.5) * 80,
                (Math.random() - 0.5) * 50
            );
            sphere.userData = {
                speedX: Math.random() * 0.02 - 0.01,
                speedY: Math.random() * 0.02 - 0.01,
                rotationSpeed: Math.random() * 0.01 - 0.005
            };
            
            // Add point light to each sphere
            const light = new THREE.PointLight(0x00f5d4, 1, 50);
            sphere.add(light);
            
            this.spheres.push(sphere);
            this.scene.add(sphere);
        }
    }
    
    addLights() {
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(10, 10, 10);
        this.scene.add(directionalLight);
    }
    
    onMouseMove(event) {
        this.mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    }
    
    handleResize() {
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Rotate particles
        if (this.particles) {
            this.particles.rotation.y += 0.0005;
            this.particles.rotation.x += 0.0002;
        }
        
        // Animate spheres
        this.spheres.forEach((sphere, index) => {
            sphere.position.x += sphere.userData.speedX + this.mouseX * 0.05;
            sphere.position.y += sphere.userData.speedY + this.mouseY * 0.05;
            sphere.rotation.x += sphere.userData.rotationSpeed;
            sphere.rotation.y += sphere.userData.rotationSpeed;
            
            // Boundary check
            if (sphere.position.x > 50 || sphere.position.x < -50) sphere.userData.speedX *= -1;
            if (sphere.position.y > 50 || sphere.position.y < -50) sphere.userData.speedY *= -1;
        });
        
        // Camera movement based on mouse
        this.camera.position.x += (this.mouseX * 5 - this.camera.position.x) * 0.02;
        this.camera.position.y += (this.mouseY * 5 - this.camera.position.y) * 0.02;
        this.camera.lookAt(this.scene.position);
        
        // Grid animation
        if (this.grid) {
            this.grid.position.x = -this.camera.position.x * 0.5;
            this.grid.position.z = -this.camera.position.z * 0.5;
        }
        
        this.renderer.render(this.scene, this.camera);
    }
}

// ============================================
// THREE.JS SHOWCASE ANIMATION
// ============================================
class ShowcaseAnimation {
    constructor() {
        this.canvas = document.getElementById('showcase-canvas');
        if (!this.canvas) return;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.canvas.offsetWidth / this.canvas.offsetHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, alpha: true, antialias: true });
        
        this.nodes = [];
        this.connections = [];
        
        this.init();
        this.animate();
        this.handleResize();
    }
    
    init() {
        this.renderer.setSize(this.canvas.offsetWidth, this.canvas.offsetHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        this.camera.position.z = 30;
        
        // Create network nodes
        this.createNodes();
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        
        const pointLight = new THREE.PointLight(0x00f5d4, 1, 100);
        pointLight.position.set(10, 10, 10);
        this.scene.add(pointLight);
    }
    
    createNodes() {
        const nodeCount = 15;
        const geometry = new THREE.OctahedronGeometry(1, 0);
        const material = new THREE.MeshPhongMaterial({
            color: 0x00f5d4,
            emissive: 0x004444,
            transparent: true,
            opacity: 0.9,
            shininess: 100
        });
        
        for (let i = 0; i < nodeCount; i++) {
            const node = new THREE.Mesh(geometry, material.clone());
            node.position.set(
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 20
            );
            node.userData = {
                rotationSpeed: {
                    x: Math.random() * 0.02 - 0.01,
                    y: Math.random() * 0.02 - 0.01
                }
            };
            
            this.nodes.push(node);
            this.scene.add(node);
        }
        
        // Create connections between nearby nodes
        this.createConnections();
    }
    
    createConnections() {
        const maxDistance = 15;
        
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const distance = this.nodes[i].position.distanceTo(this.nodes[j].position);
                
                if (distance < maxDistance) {
                    const points = [this.nodes[i].position, this.nodes[j].position];
                    const geometry = new THREE.BufferGeometry().setFromPoints(points);
                    const material = new THREE.LineBasicMaterial({
                        color: 0x00f5d4,
                        transparent: true,
                        opacity: 0.3
                    });
                    
                    const line = new THREE.Line(geometry, material);
                    this.connections.push(line);
                    this.scene.add(line);
                }
            }
        }
    }
    
    handleResize() {
        window.addEventListener('resize', () => {
            if (!this.canvas) return;
            this.camera.aspect = this.canvas.offsetWidth / this.canvas.offsetHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(this.canvas.offsetWidth, this.canvas.offsetHeight);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Rotate nodes
        this.nodes.forEach(node => {
            node.rotation.x += node.userData.rotationSpeed.x;
            node.rotation.y += node.userData.rotationSpeed.y;
        });
        
        // Update connection lines
        this.connections.forEach(line => {
            line.geometry.setFromPoints([line.geometry.attributes.position.array.slice(0, 3), 
                                         line.geometry.attributes.position.array.slice(3, 6)]);
            line.geometry.attributes.position.needsUpdate = true;
        });
        
        // Slow rotation of entire scene
        this.scene.rotation.y += 0.001;
        
        this.renderer.render(this.scene, this.camera);
    }
}

// ============================================
// GSAP SCROLL ANIMATIONS
// ============================================
function initScrollAnimations() {
    gsap.registerPlugin(ScrollTrigger);
    
    // Animate sections on scroll
    gsap.utils.toArray('section').forEach(section => {
        gsap.from(section.children, {
            scrollTrigger: {
                trigger: section,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            stagger: 0.1,
            ease: 'power3.out'
        });
    });
    
    // Animate stat numbers
    gsap.utils.toArray('.animate-count').forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        
        ScrollTrigger.create({
            trigger: counter,
            start: 'top 80%',
            once: true,
            onEnter: () => {
                gsap.to(counter, {
                    innerText: target,
                    duration: 2,
                    snap: { innerText: 1 },
                    ease: 'power2.out',
                    onUpdate: function() {
                        counter.innerText = Math.round(this.targets()[0].innerText).toLocaleString();
                    }
                });
            }
        });
    });
    
    // Parallax effect for hero visual
    gsap.to('.hero-visual', {
        scrollTrigger: {
            trigger: '.hero',
            start: 'top top',
            end: 'bottom top',
            scrub: true
        },
        y: 100,
        opacity: 0.5
    });
    
    // Feature cards stagger animation
    gsap.from('.feature-card', {
        scrollTrigger: {
            trigger: '.features-grid',
            start: 'top 75%'
        },
        y: 100,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out'
    });
    
    // Developer cards animation
    gsap.from('.dev-card', {
        scrollTrigger: {
            trigger: '.developers-grid',
            start: 'top 75%'
        },
        scale: 0.8,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: 'back.out(1.7)'
    });
}

// ============================================
// NAVIGATION FUNCTIONALITY
// ============================================
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    // Scroll effect for navbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
        
        // Close menu on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                mobileMenuBtn.querySelector('i').classList.add('fa-bars');
                mobileMenuBtn.querySelector('i').classList.remove('fa-times');
            });
        });
    }
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ============================================
// AUTH MODAL FUNCTIONALITY
// ============================================
function initAuthModal() {
    const authModal = document.getElementById('authModal');
    const loginBtn = document.getElementById('loginBtn');
    const earlyAccessBtn = document.getElementById('earlyAccessBtn');
    const heroEarlyAccess = document.getElementById('heroEarlyAccess');
    const ctaEarlyAccess = document.getElementById('ctaEarlyAccess');
    const joinWaitlist = document.getElementById('joinWaitlist');
    const modalClose = document.getElementById('modalClose');
    const googleAuth = document.getElementById('googleAuth');
    const githubAuth = document.getElementById('githubAuth');
    const authForm = document.getElementById('authForm');
    const switchToSignup = document.getElementById('switchToSignup');
    
    // Open modal functions
    const openModal = () => {
        if (authModal) authModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };
    
    const closeModal = () => {
        if (authModal) authModal.classList.remove('active');
        document.body.style.overflow = '';
    };
    
    // Event listeners
    if (loginBtn) loginBtn.addEventListener('click', openModal);
    if (earlyAccessBtn) earlyAccessBtn.addEventListener('click', openModal);
    if (heroEarlyAccess) heroEarlyAccess.addEventListener('click', openModal);
    if (ctaEarlyAccess) ctaEarlyAccess.addEventListener('click', openModal);
    if (joinWaitlist) joinWaitlist.addEventListener('click', openModal);
    
    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (authModal) {
        authModal.querySelector('.modal-backdrop').addEventListener('click', closeModal);
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && authModal.classList.contains('active')) {
                closeModal();
            }
        });
    }
    
    // Auth provider buttons (placeholder for Firebase)
    if (googleAuth) {
        googleAuth.addEventListener('click', () => {
            console.log('Google auth clicked - Implement Firebase Google Auth');
            // Example Firebase implementation:
            // const provider = new firebase.auth.GoogleAuthProvider();
            // auth.signInWithPopup(provider).then((result) => {
            //     console.log('User signed in:', result.user);
            //     closeModal();
            // }).catch((error) => {
            //     console.error('Auth error:', error);
            // });
        });
    }
    
    if (githubAuth) {
        githubAuth.addEventListener('click', () => {
            console.log('GitHub auth clicked - Implement Firebase GitHub Auth');
            // Example Firebase implementation:
            // const provider = new firebase.auth.GithubAuthProvider();
            // auth.signInWithPopup(provider).then((result) => {
            //     console.log('User signed in:', result.user);
            //     closeModal();
            // }).catch((error) => {
            //     console.error('Auth error:', error);
            // });
        });
    }
    
    // Email/password form
    if (authForm) {
        authForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            console.log('Email auth attempted:', email);
            // Example Firebase implementation:
            // auth.signInWithEmailAndPassword(email, password)
            //     .then((userCredential) => {
            //         console.log('User signed in:', userCredential.user);
            //         closeModal();
            //     })
            //     .catch((error) => {
            //         console.error('Auth error:', error);
            //     });
        });
    }
    
    // Switch to signup
    if (switchToSignup) {
        switchToSignup.addEventListener('click', (e) => {
            e.preventDefault();
            const header = document.querySelector('.auth-header h2');
            const submitBtn = authForm.querySelector('button[type="submit"]');
            
            if (header.textContent === 'Welcome Back') {
                header.textContent = 'Create Account';
                submitBtn.textContent = 'Sign Up with Email';
                switchToSignup.textContent = 'Sign in';
            } else {
                header.textContent = 'Welcome Back';
                submitBtn.textContent = 'Sign In with Email';
                switchToSignup.textContent = 'Sign up';
            }
        });
    }
}

// ============================================
// TESTIMONIAL SLIDER
// ============================================
function initTestimonialSlider() {
    const track = document.querySelector('.testimonial-track');
    const prevBtn = document.querySelector('.slider-btn.prev');
    const nextBtn = document.querySelector('.slider-btn.next');
    
    if (!track || !prevBtn || !nextBtn) return;
    
    let currentIndex = 0;
    const cards = document.querySelectorAll('.testimonial-card');
    const totalCards = cards.length;
    const visibleCards = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 768 ? 2 : 1;
    
    function updateSlider() {
        const cardWidth = cards[0].offsetWidth + 32; // 32px gap
        const offset = -currentIndex * cardWidth;
        track.style.transform = `translateX(${offset}px)`;
    }
    
    prevBtn.addEventListener('click', () => {
        currentIndex = Math.max(0, currentIndex - 1);
        updateSlider();
    });
    
    nextBtn.addEventListener('click', () => {
        currentIndex = Math.min(totalCards - visibleCards, currentIndex + 1);
        updateSlider();
    });
    
    // Handle resize
    window.addEventListener('resize', () => {
        updateSlider();
    });
}

// ============================================
// INTERACTIVE CARDS HOVER EFFECT
// ============================================
function initCardEffects() {
    // Add tilt effect to dev cards
    document.querySelectorAll('.dev-card, .why-card, .feature-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
}

// ============================================
// NEON PULSE EFFECT ON BUTTONS
// ============================================
function initButtonEffects() {
    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 40px rgba(0, 245, 212, 0.6), 0 0 80px rgba(0, 245, 212, 0.3)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 4px 20px rgba(0, 245, 212, 0.3)';
        });
    });
}

// ============================================
// LAZY LOADING FOR PERFORMANCE
// ============================================
function initLazyLoading() {
    const observerOptions = {
        root: null,
        rootMargin: '50px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
}

// ============================================
// TYPEWRITER EFFECT FOR HERO (Optional Enhancement)
// ============================================
function initTypewriterEffect() {
    const subtitle = document.querySelector('.hero-subtitle');
    if (!subtitle) return;
    
    const text = subtitle.textContent;
    subtitle.textContent = '';
    subtitle.style.borderRight = '2px solid #00f5d4';
    
    let i = 0;
    function type() {
        if (i < text.length) {
            subtitle.textContent += text.charAt(i);
            i++;
            setTimeout(type, 30);
        } else {
            subtitle.style.borderRight = 'none';
        }
    }
    
    // Start typing after a delay
    setTimeout(type, 1000);
}

// ============================================
// DATABASE INTEGRATION (Neon PostgreSQL)
// ============================================
// This is a placeholder for backend integration
// You would typically have a separate backend service handling database operations

class DatabaseService {
    constructor() {
        this.apiUrl = 'YOUR_API_ENDPOINT'; // Replace with your backend API
    }
    
    async addToWaitlist(email) {
        try {
            const response = await fetch(`${this.apiUrl}/waitlist`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Error adding to waitlist:', error);
            throw error;
        }
    }
    
    async saveUserProfile(profileData) {
        try {
            const response = await fetch(`${this.apiUrl}/profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(profileData)
            });
            
            return await response.json();
        } catch (error) {
            console.error('Error saving profile:', error);
            throw error;
        }
    }
    
    async getDeveloperProfiles(filters = {}) {
        try {
            const params = new URLSearchParams(filters).toString();
            const response = await fetch(`${this.apiUrl}/developers?${params}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching profiles:', error);
            throw error;
        }
    }
}

// ============================================
// ANALYTICS TRACKING (Optional)
// ============================================
function trackEvent(eventName, eventData = {}) {
    // Google Analytics, Mixpanel, or custom analytics
    console.log(`Event: ${eventName}`, eventData);
    
    // Example: gtag('event', eventName, eventData);
}

// Track button clicks
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            trackEvent('button_click', {
                buttonText: this.textContent.trim(),
                buttonClass: this.className
            });
        });
    });
});

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DHH - Developers Hiring Hub initialized');
    console.log('Built by Quick Red Tech Software Development Studio');
    
    // Initialize Three.js backgrounds
    new HeroBackground();
    new ShowcaseAnimation();
    
    // Initialize GSAP animations
    initScrollAnimations();
    
    // Initialize navigation
    initNavigation();
    
    // Initialize auth modal
    initAuthModal();
    
    // Initialize testimonial slider
    initTestimonialSlider();
    
    // Initialize card hover effects
    initCardEffects();
    
    // Initialize button effects
    initButtonEffects();
    
    // Initialize lazy loading
    initLazyLoading();
    
    // Optional: Typewriter effect (can be enabled/disabled)
    // initTypewriterEffect();
    
    // Track page view
    trackEvent('page_view', { page: 'landing' });
});

// ============================================
// SERVICE WORKER REGISTRATION (PWA Support)
// ============================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(registration => {
            console.log('SW registered:', registration);
        }).catch(error => {
            console.log('SW registration failed:', error);
        });
    });
}

// ============================================
// PERFORMANCE OPTIMIZATION
// ============================================
// Request idle callback for non-critical tasks
if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
        // Load non-critical resources
        console.log('Loading non-critical resources...');
    });
}

// ============================================
// EXPORT FOR MODULE USAGE
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DatabaseService,
        trackEvent
    };
}
