// AJAX cart update (feature 11) - update quantities without reload
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[action*="update_cart_item"]').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = form.action;
            const fd = new FormData(form);
            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': (window.getCookie && getCookie('csrftoken')) || '' },
                body: fd
            }).then(r => r.json()).then(data => {
                if (data.success) {
                    // update UI (simple approach: refresh cart area)
                    location.reload();
                } else {
                    alert(data.message || 'Lỗi cập nhật giỏ hàng');
                }
            }).catch(err => console.error(err));
        });
    });
});
