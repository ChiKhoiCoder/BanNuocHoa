/**
 * Search.js - Live Search with Product Suggestions
 */

let searchTimeout;
const searchInput = document.querySelector('#search-input');
const searchResults = document.querySelector('#search-results');

if (searchInput) {
    searchInput.addEventListener('input', handleSearchInput);

    // Close results when clicking outside
    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            hideSearchResults();
        }
    });
}

function handleSearchInput(e) {
    const query = e.target.value.trim();

    // Clear previous timeout
    clearTimeout(searchTimeout);

    if (query.length < 2) {
        hideSearchResults();
        return;
    }

    // Debounce search - wait 300ms after user stops typing
    searchTimeout = setTimeout(() => {
        performSearch(query);
    }, 300);
}

function performSearch(query) {
    // Show loading state
    showSearchLoading();

    fetch(`/products/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySearchResults(data.results, query);
            } else {
                hideSearchResults();
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            hideSearchResults();
        });
}

function showSearchLoading() {
    if (!searchResults) return;

    searchResults.innerHTML = `
        <div class="search-loading">
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span class="ms-2">Đang tìm kiếm...</span>
        </div>
    `;
    searchResults.classList.add('show');
}

function displaySearchResults(results, query) {
    if (!searchResults) return;

    if (results.length === 0) {
        searchResults.innerHTML = `
            <div class="search-no-results">
                <i class="fas fa-search"></i>
                <p>Không tìm thấy sản phẩm nào cho "${query}"</p>
            </div>
        `;
        searchResults.classList.add('show');
        return;
    }

    let html = '<div class="search-results-list">';

    results.forEach(product => {
        const priceHTML = formatCurrency(product.price);
        const imageHTML = product.image
            ? `<img src="${product.image}" alt="${product.name}">`
            : `<div class="no-image"><i class="fas fa-image"></i></div>`;

        const stockHTML = product.in_stock
            ? '<span class="badge bg-success">Còn hàng</span>'
            : '<span class="badge bg-danger">Hết hàng</span>';

        const ratingHTML = generateStars(product.rating);

        html += `
            <a href="${product.url}" class="search-result-item">
                <div class="result-image">
                    ${imageHTML}
                </div>
                <div class="result-details">
                    <div class="result-name">${highlightQuery(product.name, query)}</div>
                    <div class="result-brand">${product.brand}</div>
                    <div class="result-rating">${ratingHTML}</div>
                    <div class="result-footer">
                        <div class="result-price">${priceHTML}</div>
                        ${stockHTML}
                    </div>
                </div>
            </a>
        `;
    });

    html += '</div>';

    searchResults.innerHTML = html;
    searchResults.classList.add('show');
}

function hideSearchResults() {
    if (searchResults) {
        searchResults.classList.remove('show');
    }
}

function highlightQuery(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function generateStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += '<i class="fas fa-star text-warning"></i>';
        } else if (i - 0.5 <= rating) {
            stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        } else {
            stars += '<i class="far fa-star text-warning"></i>';
        }
    }
    return stars;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}
