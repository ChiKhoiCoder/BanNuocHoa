function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// AJAX add/remove wishlist
function toggleWishlist(productId, addUrl, removeUrl, button) {
    const url = button.classList.contains('added') ? removeUrl : addUrl;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(resp => resp.json())
      .then(data => {
          if (data.added || data.removed) {
              button.classList.toggle('added');
              button.innerText = button.classList.contains('added') ? 'Yêu thích ✓' : 'Yêu thích';
          }
      }).catch(err => console.error(err));
}

// Attach wishlist buttons
document.addEventListener('click', function(e) {
    const el = e.target.closest('.btn-wishlist');
    if (!el) return;
    e.preventDefault();
    const productId = el.dataset.productId;
    const addUrl = `/products/wishlist/add/${productId}/`;
    const removeUrl = `/products/wishlist/remove/${productId}/`;
    toggleWishlist(productId, addUrl, removeUrl, el);
});

// Apply coupon AJAX
document.addEventListener('DOMContentLoaded', function() {
    const applyBtn = document.getElementById('apply-coupon-btn');
    if (!applyBtn) return;
    applyBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const input = document.querySelector('input[name="coupon_code"]');
        if (!input) return;
        const code = input.value.trim();
        if (!code) {
            alert('Vui lòng nhập mã giảm giá.');
            return;
        }
        fetch('/orders/validate-coupon/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `coupon_code=${encodeURIComponent(code)}`
        }).then(r => r.json()).then(data => {
            if (data.valid) {
                const info = document.getElementById('coupon-info');
                if (info) {
                    info.innerHTML = `<div class="alert alert-success">Đã áp dụng mã: -${data.discount.toLocaleString()} ₫ — Tổng mới: ${data.new_total.toLocaleString()} ₫</div>`;
                } else {
                    alert('Mã giảm giá hợp lệ.');
                }
            } else {
                const info = document.getElementById('coupon-info');
                if (info) {
                    info.innerHTML = `<div class="alert alert-warning">${data.message}</div>`;
                } else {
                    alert(data.message);
                }
            }
        }).catch(err => console.error(err));
    });
});
