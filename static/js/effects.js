document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initMouseFollower();
    initSparkleTrail();
    initMagneticElements();
    initTextReveal();
    // initCard3DTilt();
    initGlitterEffect();
});

/**
 * Smooth Mouse Follower with Elite Glow
 */
function initMouseFollower() {
    const follower = document.createElement('div');
    follower.className = 'mouse-follower elite-cursor';
    document.body.appendChild(follower);

    let mouseX = 0, mouseY = 0;
    let followerX = 0, followerY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        follower.style.opacity = '1';
    });

    document.addEventListener('mouseleave', () => {
        follower.style.opacity = '0';
    });

    const animate = () => {
        followerX += (mouseX - followerX) * 0.15;
        followerY += (mouseY - followerY) * 0.15;
        follower.style.transform = `translate(${followerX - 10}px, ${followerY - 10}px)`;
        requestAnimationFrame(animate);
    };
    animate();

    // Scale up on links
    const links = document.querySelectorAll('a, button, .clickable, .card-3d');
    links.forEach(link => {
        link.addEventListener('mouseenter', () => {
            follower.classList.add('active');
        });
        link.addEventListener('mouseleave', () => {
            follower.classList.remove('active');
        });
    });
}

/**
 * Magic Sparkle Trail
 */
function initSparkleTrail() {
    let lastX = 0;
    let lastY = 0;

    document.addEventListener('mousemove', (e) => {
        const distance = Math.hypot(e.clientX - lastX, e.clientY - lastY);
        
        if (distance > 15) {
            createSparkle(e.clientX, e.clientY);
            lastX = e.clientX;
            lastY = e.clientY;
        }
    });

    function createSparkle(x, y) {
        const sparkle = document.createElement('div');
        sparkle.className = 'magic-sparkle';
        const size = Math.random() * 8 + 4;
        
        sparkle.style.width = `${size}px`;
        sparkle.style.height = `${size}px`;
        sparkle.style.left = `${x}px`;
        sparkle.style.top = `${y}px`;
        
        // Random drift
        const dx = (Math.random() - 0.5) * 50;
        const dy = (Math.random() - 0.5) * 50;
        sparkle.style.setProperty('--dx', `${dx}px`);
        sparkle.style.setProperty('--dy', `${dy}px`);
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => {
            sparkle.remove();
        }, 1000);
    }
}

/**
 * Glitter Burst on Hover
 */
function initGlitterEffect() {
    const elements = document.querySelectorAll('.glitter-hover');
    
    elements.forEach(el => {
        el.addEventListener('mouseenter', (e) => {
            for (let i = 0; i < 15; i++) {
                createSparkleBurst(e.clientX, e.clientY);
            }
        });
    });

    function createSparkleBurst(x, y) {
        const sparkle = document.createElement('div');
        sparkle.className = 'magic-sparkle burst';
        const size = Math.random() * 6 + 2;
        
        sparkle.style.width = `${size}px`;
        sparkle.style.height = `${size}px`;
        sparkle.style.left = `${x}px`;
        sparkle.style.top = `${y}px`;
        
        const angle = Math.random() * Math.PI * 2;
        const velocity = Math.random() * 100 + 50;
        const dx = Math.cos(angle) * velocity;
        const dy = Math.sin(angle) * velocity;
        
        sparkle.style.setProperty('--dx', `${dx}px`);
        sparkle.style.setProperty('--dy', `${dy}px`);
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => sparkle.remove(), 800);
    }
}

/**
 * Magnetic Button Effect
 */
function initMagneticElements() {
    const magneticItems = document.querySelectorAll('.magnetic-wrap');

    magneticItems.forEach(item => {
        item.addEventListener('mousemove', (e) => {
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            item.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });

        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translate(0px, 0px)';
        });
    });
}

/**
 * Text Reveal on Scroll
 */
function initTextReveal() {
    const revealItems = document.querySelectorAll('.text-reveal');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    revealItems.forEach(item => observer.observe(item));
}


/**
 * Dark/Light Mode Toggle with Persistence
 */
function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    // Load saved theme
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateToggleIcon(currentTheme);

    toggleBtn.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleIcon(newTheme);

        // Add a "burst" effect on toggle
        for(let i=0; i<20; i++) {
            createThemeSparkle(window.innerWidth/2, window.innerHeight/2);
        }
    });

    function updateToggleIcon(theme) {
        const icon = toggleBtn.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill';
            toggleBtn.style.color = '#fbbf24';
        } else {
            icon.className = 'bi bi-moon-stars-fill';
            toggleBtn.style.color = '#6366f1';
        }
    }

    function createThemeSparkle(x, y) {
        const s = document.createElement('div');
        s.className = 'magic-sparkle burst';
        s.style.left = `${x}px`;
        s.style.top = `${y}px`;
        s.style.background = 'var(--primary-color)';
        document.body.appendChild(s);
        setTimeout(() => s.remove(), 1000);
    }
}

/**
 * Optimized 3D Card Tilt - Ensures images remain stable as per user request
 */
function initCard3DTilt() {
    const cards = document.querySelectorAll('.card-3d');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Very subtle tilt for the CONTAINER only
            const rotateX = (centerY - y) / 25;
            const rotateY = (x - centerX) / 25;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            
            // Ensure child images don't move (counter-acting tilt if needed)
            const img = card.querySelector('.product-main-img');
            if (img) {
                img.style.transform = 'translateZ(0) scale(1)';
            }
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
        });
    });
}
