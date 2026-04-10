/**
 * Cart.js - Advanced Cart Management with AJAX
 * Features: Mini Cart Dropdown, Real-time Updates, Notifications
 */

// Notification library (using Notyf for modern notifications)
let notyf;

document.addEventListener('DOMContentLoaded', function () {
    // Initialize notification library
    notyf = new Notyf({
        duration: 3000,
        position: { x: 'right', y: 'top' },
        dismissible: true
    });

    // Initialize cart
    initializeCart();
    loadMiniCart();

    // Event listeners
    setupCartEventListeners();
});

/**
 * Initialize cart functionality
 */
function initializeCart() {
    // Update cart count on page load
    updateCartCount();

    // Mini cart hover functionality
    const cartIcon = document.querySelector('.cart-icon');
    const miniCart = document.querySelector('.mini-cart-dropdown');

    if (cartIcon && miniCart) {
        let hideTimeout;

        cartIcon.addEventListener('mouseenter', function () {
            clearTimeout(hideTimeout);
            loadMiniCart();
            miniCart.classList.add('show');
        });

        cartIcon.addEventListener('mouseleave', function () {
            hideTimeout = setTimeout(() => {
                miniCart.classList.remove('show');
            }, 300);
        });

        miniCart.addEventListener('mouseenter', function () {
            clearTimeout(hideTimeout);
        });

        miniCart.addEventListener('mouseleave', function () {
            hideTimeout = setTimeout(() => {
                miniCart.classList.remove('show');
            }, 300);
        });
    }
}

/**
 * Setup event listeners for cart actions
 */
function setupCartEventListeners() {
    // Add to cart buttons
    document.querySelectorAll('.btn-add-to-cart').forEach(btn => {
        btn.addEventListener('click', handleAddToCart);
    });

    // Update quantity buttons (in cart page)
    document.querySelectorAll('.update-quantity-btn').forEach(btn => {
        btn.addEventListener('click', handleUpdateQuantity);
    });

    // Remove item buttons
    document.querySelectorAll('.remove-item-btn').forEach(btn => {
        btn.addEventListener('click', handleRemoveItem);
    });

    // Quantity input changes
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', handleQuantityChange);
    });
}

/**
 * Load mini cart data via AJAX
 */
function loadMiniCart() {
    fetch('/carts/api/get/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderMiniCart(data);
            }
        })
        .catch(error => {
            console.error('Error loading mini cart:', error);
        });
}

/**
 * Render mini cart dropdown
 */
function renderMiniCart(data) {
    const miniCartBody = document.querySelector('.mini-cart-body');
    const miniCartFooter = document.querySelector('.mini-cart-footer');

    if (!miniCartBody) return;

    if (data.items.length === 0) {
        miniCartBody.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <p class="text-muted">Giỏ hàng trống</p>
            </div>
        `;
        if (miniCartFooter) {
            miniCartFooter.style.display = 'none';
        }
        return;
    }

    let itemsHTML = '';
    data.items.forEach(item => {
        itemsHTML += `
            <div class="mini-cart-item" data-item-id="${item.id}">
                <div class="item-image">
                    <img src="${item.product_image || '/static/images/no-image.png'}" alt="${item.product_name}">
                </div>
                <div class="item-details">
                    <h6 class="item-name">${item.product_name}</h6>
                    <div class="item-price">${formatCurrency(item.price)} × ${item.quantity}</div>
                    <div class="item-total fw-bold">${formatCurrency(item.total)}</div>
                </div>
                <button class="btn-remove-mini" data-confirm="Bạn muốn xóa sản phẩm này không?"
                    onclick="removeFromCart(${item.id}, { skipConfirm: true })">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    });

    miniCartBody.innerHTML = itemsHTML;

    if (miniCartFooter) {
        miniCartFooter.style.display = 'block';
        miniCartFooter.querySelector('.cart-total-amount').textContent = formatCurrency(data.total);
    }

    updateCartCount(data.count);
}

/**
 * Handle add to cart
 */
function handleAddToCart(e) {
    e.preventDefault();

    const btn = e.currentTarget;
    const productId = btn.dataset.productId;
    const quantityInput = document.querySelector(`#quantity-${productId}`);
    const quantity = quantityInput ? quantityInput.value : 1;

    // Disable button
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang thêm...';

    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    fetch(`/carts/api/add/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `quantity=${quantity}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notyf.success(data.message);
                updateCartCount(data.cart_count);
                loadMiniCart();

                // Animate cart icon
                animateCartIcon();
            } else {
                notyf.error(data.message);
            }
        })
        .catch(error => {
            notyf.error('Có lỗi xảy ra. Vui lòng thử lại.');
            console.error('Error:', error);
        })
        .finally(() => {
            // Re-enable button
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-shopping-cart"></i> Thêm vào giỏ';
        });
}

/**
 * Handle update quantity
 */
async function handleQuantityChange(e) {
    const input = e.target;
    const itemId = input.dataset.itemId;
    const quantity = parseInt(input.value);

    if (quantity < 1) {
        const ask = window.confirmAction
            ? window.confirmAction('Bạn muốn xóa sản phẩm này không?')
            : Promise.resolve(confirm('Bạn có muốn xóa sản phẩm này khỏi giỏ hàng?'));

        if (await ask) {
            removeFromCart(itemId, { skipConfirm: true });
        } else {
            input.value = 1;
        }
        return;
    }

    updateCartItem(itemId, quantity);
}

/**
 * Update cart item quantity via AJAX
 */
function updateCartItem(itemId, quantity) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/carts/api/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `quantity=${quantity}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.deleted) {
                    // Remove item from DOM
                    document.querySelector(`[data-cart-item="${itemId}"]`)?.remove();
                    notyf.success(data.message);
                } else {
                    // Update totals
                    const itemTotalElement = document.querySelector(`#item-total-${itemId}`);
                    if (itemTotalElement) {
                        itemTotalElement.textContent = formatCurrency(data.item_total);
                    }

                    const cartTotalElement = document.querySelector('#cart-total');
                    if (cartTotalElement) {
                        cartTotalElement.textContent = formatCurrency(data.cart_total);
                    }

                    notyf.success(data.message);
                }

                updateCartCount(data.cart_count);
                loadMiniCart();
            } else {
                notyf.error(data.message);
            }
        })
        .catch(error => {
            notyf.error('Có lỗi xảy ra. Vui lòng thử lại.');
            console.error('Error:', error);
        });
}

/**
 * Remove item from cart
 */
function removeFromCart(itemId, options = {}) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/carts/api/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove from DOM
                document.querySelector(`[data-cart-item="${itemId}"]`)?.remove();
                document.querySelector(`[data-item-id="${itemId}"]`)?.remove();

                // Update total
                const cartTotalElement = document.querySelector('#cart-total');
                if (cartTotalElement) {
                    cartTotalElement.textContent = formatCurrency(data.cart_total);
                }

                updateCartCount(data.cart_count);
                loadMiniCart();
                notyf.success(data.message);

                // Check if cart is empty
                if (data.cart_count === 0) {
                    const cartContainer = document.querySelector('.cart-items-container');
                    if (cartContainer) {
                        cartContainer.innerHTML = `
                        <div class="empty-cart text-center py-5">
                            <i class="fas fa-shopping-cart fa-4x text-muted mb-3"></i>
                            <h4>Giỏ hàng trống</h4>
                            <a href="/products/" class="btn btn-primary mt-3">Tiếp tục mua sắm</a>
                        </div>
                    `;
                    }
                }
            } else {
                notyf.error(data.message);
            }
        })
        .catch(error => {
            notyf.error('Có lỗi xảy ra. Vui lòng thử lại.');
            console.error('Error:', error);
        });
}

/**
 * Update cart count badge
 */
function updateCartCount(count) {
    if (count === undefined) {
        // Fetch count from server
        fetch('/carts/api/get/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartBadge(data.count);
                }
            });
    } else {
        updateCartBadge(count);
    }
}

function updateCartBadge(count) {
    const badge = document.querySelector('.cart-count-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
}

/**
 * Animate cart icon when item added
 */
function animateCartIcon() {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.classList.add('cart-bounce');
        setTimeout(() => {
            cartIcon.classList.remove('cart-bounce');
        }, 500);
    }
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

/**
 * Get CSRF token from cookie
 */
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

/**
 * Handle remove item button click
 */
async function handleRemoveItem(e) {
    e.preventDefault();
    const btn = e.currentTarget;
    const itemId = btn.dataset.itemId;

    const ask = window.confirmAction
        ? window.confirmAction('Bạn muốn xóa sản phẩm này không?')
        : Promise.resolve(confirm('Bạn có chắc muốn xóa sản phẩm này?'));

    if (await ask) {
        removeFromCart(itemId, { skipConfirm: true });
    }
}

/**
 * Handle update quantity button click
 */
function handleUpdateQuantity(e) {
    e.preventDefault();
    const btn = e.currentTarget;
    const itemId = btn.dataset.itemId;
    const input = document.querySelector(`#quantity-${itemId}`);
    const quantity = parseInt(input.value);

    updateCartItem(itemId, quantity);
}
