// Tag filter quick links (feature 16)
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tag-filter').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const tag = this.dataset.tag;
            const url = new URL(window.location.href);
            url.searchParams.set('tag', tag);
            fetch(url.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.text()).then(html => {
                    const list = document.querySelector('.product-list-container');
                    if (list) list.innerHTML = html;
                });
        });
    });
});
