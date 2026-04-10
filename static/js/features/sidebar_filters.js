// Sidebar filters UI (feature 15) - range slider + checkboxes (frontend)
document.addEventListener('DOMContentLoaded', function () {
    const range = document.querySelector('input[type="range"][name="price_range"]');
    if (range) {
        const display = document.createElement('div');
        display.className = 'small text-muted';
        range.parentNode.appendChild(display);
        range.addEventListener('input', () => { display.innerText = `<= ${parseInt(range.value).toLocaleString()} ₫`; });
    }

    // wire filter form to AJAX submit
    const filterForm = document.querySelector('form[name="product_filters"]');
    if (!filterForm) return;
    filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const fd = new FormData(filterForm);
        const params = new URLSearchParams();
        for (const [k,v] of fd.entries()) params.append(k,v);
        fetch(`/products/?${params.toString()}`, { headers: { 'X-Requested-With':'XMLHttpRequest' }})
            .then(r => r.text()).then(html => {
                const list = document.querySelector('.product-list-container');
                if (list) list.innerHTML = html;
            });
    });
});
