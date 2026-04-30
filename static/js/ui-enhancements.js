/**
 * UI Enhancements - Modern Effects and Interactions
 * Includes: Scroll animations, Back to top, Sticky header, Breadcrumbs
 */

document.addEventListener('DOMContentLoaded', function () {
    initializeAOS();
    initializeBackToTop();
    initializeStickyHeader();
    initializeParallax();
    initializeLazyLoading();
    initializeMiniCart();
});

/**
 * Mini-cart dropdown hover behaviour + add-to-cart AJAX skeleton
 */
function initializeMiniCart() {
    const miniCartToggle = document.getElementById('miniCartToggle');
    const miniCartContainer = document.getElementById('mini-cart-container');

    if (!miniCartToggle || !miniCartContainer) return;

    // Show dropdown on hover for desktop
    miniCartContainer.addEventListener('mouseenter', () => {
        miniCartToggle.click();
    });

    // Add-to-cart buttons
    document.addEventListener('click', function (e) {
        const t = e.target.closest('.add-to-cart');
        if (!t) return;
        const productId = t.dataset.productId;
        const card = t.closest('.product-card') || t.closest('.product-luxe-card') || document;
        const selectedVolume = card.querySelector('.volume-btn.active')?.dataset?.volume || '30';

        // Optimistic UI: show loader on button
        t.disabled = true;
        t.innerText = 'Đang thêm...';

        // POST form data to carts AJAX endpoint
        const formData = new FormData();
        formData.append('quantity', 1);
        formData.append('volume', selectedVolume);

        fetch(`/carts/api/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        }).then(r => r.json()).then(data => {
            if (!data.success) {
                alert(data.message || 'Lỗi khi thêm vào giỏ');
                return;
            }
            // Mua Ngay: Redirect to checkout immediately
            window.location.href = '/checkout/';
        }).catch(err => {
            console.error('Add to cart failed', err);
            alert('Lỗi kết nối. Vui lòng thử lại.');
        }).finally(() => {
            t.disabled = false;
        });
    });
}

/**
 * Simple helper to get cookie value (for CSRF)
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
/**
 * Initialize AOS (Animate On Scroll)
 */
function initializeAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100,
            delay: 100,
        });
    }
}

/**
 * Back to Top Button
 */
function initializeBackToTop() {
    // Create back to top button
    const backToTop = document.createElement('button');
    backToTop.id = 'back-to-top';
    backToTop.className = 'back-to-top-btn';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTop);

    // Show/hide on scroll
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });

    // Scroll to top on click
    backToTop.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Sticky Header
 */
function initializeStickyHeader() {
    const header = document.querySelector('header');
    if (!header) return;

    let lastScroll = 0;
    const headerHeight = header.offsetHeight;
    let ticking = false;

    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(function () {
                const currentScroll = window.pageYOffset;

                if (currentScroll > headerHeight) {
                    header.classList.add('sticky');
                } else {
                    header.classList.remove('sticky');
                }

                lastScroll = currentScroll;
                ticking = false;
            });
            ticking = true;
        }
    });
}

/**
 * Parallax Effect for Hero Sections
 */
function initializeParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');

    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', function () {
        const scrolled = window.pageYOffset;

        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Lazy Loading Images
 */
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

/**
 * Smooth Scroll for Anchor Links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);

        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * Add entrance animations to elements
 */
function addEntranceAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(el => observer.observe(el));
}

/**
 * Background Particle System
 */
function initParticles() {
    const container = document.getElementById('particle-container');
    if (!container) return;

    const particleCount = 20;
    const colors = ['#10b981', '#f97316', '#fbbf24', '#ffffff'];

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random styles
        const size = Math.random() * 15 + 5;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const left = Math.random() * 100;
        const delay = Math.random() * 20;
        const duration = Math.random() * 10 + 15;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${left}%`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        particle.style.setProperty('--particle-color', color);

        container.appendChild(particle);
    }
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    if (document.querySelector('.animate-on-scroll')) {
        addEntranceAnimations();
    }
});
