// Search suggestions (feature 14)
document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[name="query"]');
    if (!input) return;
    const box = document.createElement('div');
    box.className = 'search-suggestions-box card p-2';
    box.style.position = 'absolute';
    box.style.zIndex = 1060;
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(box);

    let timeout;
    input.addEventListener('input', function () {
        clearTimeout(timeout);
        const q = this.value.trim();
        if (!q) { box.innerHTML = ''; return; }
        timeout = setTimeout(() => {
            fetch(`/api/search_suggestions/?q=${encodeURIComponent(q)}`)
                .then(r => r.json()).then(data => {
                    box.innerHTML = '';
                    (data.results || []).slice(0,6).forEach(p => {
                        const el = document.createElement('a');
                        el.href = `/products/${p.id}/`;
                        el.className = 'd-flex align-items-center gap-2 p-2 text-decoration-none text-dark';
                        el.innerHTML = `<img src="${p.image||'/static/images/placeholder.png'}" style="width:40px;height:40px;object-fit:cover;border-radius:6px;"> <div><div>${p.name}</div><small class='text-muted'>${p.price.toLocaleString()} ₫</small></div>`;
                        box.appendChild(el);
                    });
                });
        }, 200);
    });
});
