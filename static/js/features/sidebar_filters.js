/**
 * Enhanced Sidebar Filters JS
 * Handles price slider, AJAX filtering and UI interactions
 */
document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.querySelector('form[name="product_filters"]');
    if (!filterForm) return;

    // Price Slider Initialization (Assuming noUiSlider is available)
    const priceSlider = document.getElementById('price-slider');
    if (priceSlider && typeof noUiSlider !== 'undefined') {
        noUiSlider.create(priceSlider, {
            start: [
                parseInt(document.getElementById('min-price-input').value) || 0,
                parseInt(document.getElementById('max-price-input').value) || 10000000
            ],
            connect: true,
            step: 100000,
            range: {
                'min': 0,
                'max': 10000000
            },
            format: {
                to: value => Math.round(value),
                from: value => Number(value)
            }
        });

        const minDisplay = document.getElementById('min-price-display');
        const maxDisplay = document.getElementById('max-price-display');
        const minInput = document.getElementById('min-price-input');
        const maxInput = document.getElementById('max-price-input');

        priceSlider.noUiSlider.on('update', function (values, handle) {
            const val = parseInt(values[handle]);
            if (handle === 0) {
                minDisplay.textContent = val.toLocaleString() + '₫';
                minInput.value = val;
            } else {
                maxDisplay.textContent = val.toLocaleString() + '₫';
                maxInput.value = val;
            }
        });

        // Trigger filter on change
        priceSlider.noUiSlider.on('change', function() {
            filterForm.dispatchEvent(new Event('submit'));
        });
    }

    // AJAX Filtering
    filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        // Show loading state in product container
        const productContainer = document.getElementById('products-container');
        if (productContainer) {
            productContainer.style.opacity = '0.5';
            productContainer.style.pointerEvents = 'none';
        }

        const formData = new FormData(filterForm);
        const params = new URLSearchParams();
        
        for (const [key, value] of formData.entries()) {
            if (value) params.append(key, value);
        }

        const url = `${window.location.pathname}?${params.toString()}`;
        
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Update products
            const newProducts = doc.getElementById('products-container');
            if (newProducts && productContainer) {
                productContainer.innerHTML = newProducts.innerHTML;
                productContainer.style.opacity = '1';
                productContainer.style.pointerEvents = 'auto';
                
                // Re-initialize AOS if available
                if (typeof AOS !== 'undefined') {
                    AOS.refresh();
                }
            }

            // Update pagination
            const oldPagination = document.getElementById('pagination-container');
            const newPagination = doc.getElementById('pagination-container');
            if (oldPagination && newPagination) {
                oldPagination.innerHTML = newPagination.innerHTML;
            } else if (oldPagination && !newPagination) {
                oldPagination.innerHTML = '';
            }

            // Update URL without reloading
            window.history.pushState({}, '', url);
        })
        .catch(error => {
            console.error('Error fetching filters:', error);
            if (productContainer) {
                productContainer.style.opacity = '1';
                productContainer.style.pointerEvents = 'auto';
            }
        });
    });

    // Auto-submit on checkbox/select change
    filterForm.querySelectorAll('input[type="checkbox"], select').forEach(el => {
        el.addEventListener('change', () => {
            filterForm.dispatchEvent(new Event('submit'));
        });
    });

    // Handle "Clear All" link
    const clearLink = document.querySelector('.clear-all-link');
    if (clearLink) {
        clearLink.addEventListener('click', function(e) {
            e.preventDefault();
            filterForm.reset();
            
            // Reset price slider if exists
            if (priceSlider && priceSlider.noUiSlider) {
                priceSlider.noUiSlider.set([0, 10000000]);
            }
            
            // Clear inputs manually if reset() doesn't cover hidden fields
            filterForm.querySelectorAll('input[type="hidden"]').forEach(input => input.value = '');
            
            filterForm.dispatchEvent(new Event('submit'));
        });
    }
});
