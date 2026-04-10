// Back to Top (feature 18) - created separately for modularity
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;
    btn.addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top:0, behavior:'smooth' }); });
});
