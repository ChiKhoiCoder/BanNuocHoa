// Mini Cart Dropdown (feature 10)
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('mini-cart-container');
    if (!container) return;
    // open on hover (desktop)
    container.addEventListener('mouseenter', () => {
        const toggle = container.querySelector('[data-bs-toggle="dropdown"]');
        if (toggle && !toggle.classList.contains('show')) toggle.click();
    });
    container.addEventListener('mouseleave', () => {
        const toggle = container.querySelector('[data-bs-toggle="dropdown"]');
        if (toggle && toggle.classList.contains('show')) toggle.click();
    });
});
