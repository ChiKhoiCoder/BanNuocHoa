// Checkout progress UI (feature 12)
document.addEventListener('DOMContentLoaded', function () {
    const bar = document.querySelector('.checkout-progress');
    if (!bar) return;
    const steps = bar.querySelectorAll('.step');
    function setStep(index) {
        steps.forEach((s, i) => {
            s.classList.toggle('active', i <= index);
        });
    }
    // expose for pages
    window.checkoutProgressSet = setStep;
});
