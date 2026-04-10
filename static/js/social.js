/**
 * Social.js - Social Sharing & Engagement Features
 */

/**
 * Social Media Sharing
 */
function shareOnFacebook(url, title) {
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    openShareWindow(shareUrl);
}

function shareOnTwitter(url, title) {
    const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
    openShareWindow(shareUrl);
}

function shareOnZalo(url, title) {
    const shareUrl = `https://sp.zalo.me/share_inline?url=${encodeURIComponent(url)}`;
    openShareWindow(shareUrl);
}

function copyLink(url) {
    navigator.clipboard.writeText(url).then(() => {
        if (typeof notyf !== 'undefined') {
            notyf.success('Đã sao chép link!');
        } else {
            alert('Đã sao chép link!');
        }
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function openShareWindow(url) {
    window.open(url, 'share', 'width=600,height=400,scrollbars=yes');
}

/**
 * Setup share buttons
 */
document.addEventListener('DOMContentLoaded', function () {
    // Facebook share buttons
    document.querySelectorAll('.share-facebook').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            shareOnFacebook(url, title);
        });
    });

    // Twitter share buttons
    document.querySelectorAll('.share-twitter').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            shareOnTwitter(url, title);
        });
    });

    // Zalo share buttons
    document.querySelectorAll('.share-zalo').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            shareOnZalo(url, title);
        });
    });

    // Copy link buttons
    document.querySelectorAll('.copy-link').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            copyLink(url);
        });
    });

    // Initialize view counter
    initializeViewCounter();

    // Initialize purchase notifications
    initializePurchaseNotifications();
});

/**
 * Product View Counter
 */
function initializeViewCounter() {
    const viewCounter = document.querySelector('.view-counter');
    if (!viewCounter) return;

    const productId = viewCounter.dataset.productId;
    if (!productId) return;

    // Track view
    fetch(`/products/api/track-view/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateViewCount(data.view_count);
            }
        })
        .catch(error => console.error('Error tracking view:', error));

    // Update view count periodically
    setInterval(() => {
        fetch(`/products/api/view-count/${productId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateViewCount(data.view_count);
                }
            });
    }, 30000); // Update every 30 seconds
}

function updateViewCount(count) {
    const viewCounter = document.querySelector('.view-counter');
    if (viewCounter) {
        viewCounter.textContent = `${count} người đang xem`;

        // Animate counter
        viewCounter.classList.add('pulse');
        setTimeout(() => viewCounter.classList.remove('pulse'), 500);
    }
}

/**
 * Purchase Notification Popups
 */
function initializePurchaseNotifications() {
    // Check if we should show notifications
    if (!document.querySelector('.product-detail-page') &&
        !document.querySelector('.product-list-page')) {
        return;
    }

    // Fetch recent purchases
    fetchRecentPurchases();

    // Show notifications periodically
    setInterval(() => {
        fetchRecentPurchases();
    }, 60000); // Every minute
}

function fetchRecentPurchases() {
    fetch('/products/api/recent-purchases/')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.purchases.length > 0) {
                showPurchaseNotification(data.purchases[0]);
            }
        })
        .catch(error => console.error('Error fetching purchases:', error));
}

function showPurchaseNotification(purchase) {
    // Don't show if user just made this purchase
    const lastPurchaseId = sessionStorage.getItem('lastPurchaseId');
    if (lastPurchaseId == purchase.id) return;

    const notification = document.createElement('div');
    notification.className = 'purchase-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-image">
                <img src="${purchase.product_image || '/static/images/no-image.png'}" alt="${purchase.product_name}">
            </div>
            <div class="notification-text">
                <div class="notification-title">Vừa có người mua!</div>
                <div class="notification-product">${purchase.product_name}</div>
                <div class="notification-location">
                    <i class="fas fa-map-marker-alt"></i> ${purchase.location}
                </div>
                <div class="notification-time">${purchase.time_ago}</div>
            </div>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);

    // Auto hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Get CSRF token
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
