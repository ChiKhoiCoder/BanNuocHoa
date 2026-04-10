// Address autocomplete (feature 13) - frontend only, calls /api/address_suggest/?q=
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[data-autocomplete="address"]');
    if (!inputs) return;

    inputs.forEach(input => {
        const box = document.createElement('div');
        box.className = 'autocomplete-box';
        box.style.position = 'absolute';
        box.style.zIndex = 1050;
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(box);

        let timeout;
        input.addEventListener('input', function () {
            clearTimeout(timeout);
            const q = this.value.trim();
            if (!q) { box.innerHTML = ''; return; }
            timeout = setTimeout(() => {
                fetch(`/api/address_suggest/?q=${encodeURIComponent(q)}`)
                    .then(r => r.json()).then(data => {
                        box.innerHTML = '';
                        if (data.suggestions) {
                            data.suggestions.forEach(s => {
                                const el = document.createElement('div');
                                el.className = 'p-2 suggestion-item';
                                el.style.cursor = 'pointer';
                                el.innerText = s;
                                el.addEventListener('click', () => { input.value = s; box.innerHTML = ''; });
                                box.appendChild(el);
                            });
                        }
                    });
            }, 250);
        });
    });
});
