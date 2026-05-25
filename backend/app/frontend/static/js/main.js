gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
    // Hero Animations
    const tl = gsap.timeline();
    
    tl.from('.logo', {
        y: -20,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    })
    .from('nav ul li', {
        y: -20,
        opacity: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: 'power3.out'
    }, '-=0.5')
    .from('.auth-btns', {
        x: 20,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    }, '-=0.5');

    // Reveal elements on scroll
    gsap.utils.toArray('.reveal').forEach(el => {
        gsap.to(el, {
            scrollTrigger: {
                trigger: el,
                start: 'top 85%',
                toggleActions: 'play none none none'
            },
            y: 0,
            opacity: 1,
            duration: 1,
            ease: 'power3.out'
        });
    });

    // Gradient text animation
    gsap.to('.gradient-text', {
        backgroundPosition: '200% center',
        duration: 4,
        repeat: -1,
        ease: 'linear'
    });

    // Mouse movement glow effect
    document.addEventListener('mousemove', (e) => {
        const glows = document.querySelectorAll('.glow');
        const mouseX = e.clientX;
        const mouseY = e.clientY;

        glows.forEach((glow, index) => {
            const speed = (index + 1) * 0.02;
            const x = (window.innerWidth - mouseX * speed) / 100;
            const y = (window.innerHeight - mouseY * speed) / 100;
            
            gsap.to(glow, {
                x: x * 20,
                y: y * 20,
                duration: 1,
                ease: 'power2.out'
            });
        });
    });
});
