/**
 * Filters.js - Professional Sidebar Filters with AJAX
 */

class ProductFilters {
    constructor() {
        this.filters = {
            category: null,
            min_price: null,
            max_price: null,
            brands: [],
            scent_types: [],
            tags: [],
            sort: 'name',
            page: 1
        };

        this.priceSlider = null;
        this.init();
    }

    init() {
        this.loadFilterOptions();
        this.setupPriceSlider();
        this.setupEventListeners();
        this.loadUrlParams();
    }

    loadFilterOptions() {
        const categoryId = document.querySelector('[data-category-id]')?.dataset.categoryId;
        const url = categoryId
            ? `/products/api/filter-options/?category=${categoryId}`
            : '/products/api/filter-options/';

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.renderFilterOptions(data);
                }
            })
            .catch(error => console.error('Error loading filter options:', error));
    }

    renderFilterOptions(data) {
        // Render brands
        const brandsContainer = document.querySelector('#brands-filter');
        if (brandsContainer && data.brands) {
            let html = '';
            data.brands.forEach(brand => {
                html += `
                    <div class="form-check">
                        <input class="form-check-input brand-checkbox" type="checkbox" 
                               value="${brand}" id="brand-${brand}">
                        <label class="form-check-label" for="brand-${brand}">
                            ${brand}
                        </label>
                    </div>
                `;
            });
            brandsContainer.innerHTML = html;
        }

        // Render scent types
        const scentContainer = document.querySelector('#scent-filter');
        if (scentContainer && data.scent_types) {
            let html = '';
            data.scent_types.forEach(scent => {
                html += `
                    <div class="form-check">
                        <input class="form-check-input scent-checkbox" type="checkbox" 
                               value="${scent}" id="scent-${scent}">
                        <label class="form-check-label" for="scent-${scent}">
                            ${scent}
                        </label>
                    </div>
                `;
            });
            scentContainer.innerHTML = html;
        }

        // Update price slider range
        if (data.price_range && this.priceSlider) {
            this.priceSlider.updateOptions({
                range: {
                    'min': data.price_range.min,
                    'max': data.price_range.max
                },
                start: [data.price_range.min, data.price_range.max]
            });
        }
    }

    setupPriceSlider() {
        const sliderElement = document.getElementById('price-slider');
        if (!sliderElement) return;

        this.priceSlider = noUiSlider.create(sliderElement, {
            start: [0, 10000000],
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

        // Update price display
        const minPriceDisplay = document.getElementById('min-price-display');
        const maxPriceDisplay = document.getElementById('max-price-display');

        this.priceSlider.on('update', (values) => {
            if (minPriceDisplay) minPriceDisplay.textContent = this.formatPrice(values[0]);
            if (maxPriceDisplay) maxPriceDisplay.textContent = this.formatPrice(values[1]);
        });

        // Apply filter on change
        this.priceSlider.on('change', (values) => {
            this.filters.min_price = values[0];
            this.filters.max_price = values[1];
            this.applyFilters();
        });
    }

    setupEventListeners() {
        // Brand checkboxes
        document.querySelectorAll('.brand-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', () => this.handleBrandChange());
        });

        // Scent type checkboxes
        document.querySelectorAll('.scent-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', () => this.handleScentChange());
        });

        // Tag buttons
        document.querySelectorAll('.tag-filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleTagClick(e));
        });

        // Sort dropdown
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.filters.sort = e.target.value;
                this.applyFilters();
            });
        }

        // Clear filters button
        const clearBtn = document.getElementById('clear-filters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearFilters());
        }
    }

    handleBrandChange() {
        this.filters.brands = Array.from(document.querySelectorAll('.brand-checkbox:checked'))
            .map(cb => cb.value);
        this.applyFilters();
    }

    handleScentChange() {
        this.filters.scent_types = Array.from(document.querySelectorAll('.scent-checkbox:checked'))
            .map(cb => cb.value);
        this.applyFilters();
    }

    handleTagClick(e) {
        e.preventDefault();
        const tag = e.currentTarget.dataset.tag;

        if (this.filters.tags.includes(tag)) {
            this.filters.tags = this.filters.tags.filter(t => t !== tag);
            e.currentTarget.classList.remove('active');
        } else {
            this.filters.tags.push(tag);
            e.currentTarget.classList.add('active');
        }

        this.applyFilters();
    }

    applyFilters() {
        // Show loading state
        this.showLoading();

        // Build query string
        const params = new URLSearchParams();

        if (this.filters.category) params.append('category', this.filters.category);
        if (this.filters.min_price) params.append('min_price', this.filters.min_price);
        if (this.filters.max_price) params.append('max_price', this.filters.max_price);
        this.filters.brands.forEach(b => params.append('brand', b));
        this.filters.scent_types.forEach(s => params.append('scent_type', s));
        this.filters.tags.forEach(t => params.append('tag', t));
        params.append('sort', this.filters.sort);
        params.append('page', this.filters.page);

        // Fetch filtered products
        fetch(`/products/api/filter/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.renderProducts(data.results);
                    this.renderPagination(data.pagination);
                    this.updateUrl(params);
                }
            })
            .catch(error => {
                console.error('Filter error:', error);
                this.hideLoading();
            });
    }

    renderProducts(products) {
        const container = document.getElementById('products-container');
        if (!container) return;

        if (products.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4>Không tìm thấy sản phẩm</h4>
                    <p class="text-muted">Vui lòng thử điều chỉnh bộ lọc</p>
                </div>
            `;
            this.hideLoading();
            return;
        }

        let html = '';
        products.forEach(product => {
            html += this.renderProductCard(product);
        });

        container.innerHTML = html;
        this.hideLoading();

        // Scroll to top of products
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    renderProductCard(product) {
        const priceHTML = product.discount_price
            ? `<del class="text-muted">${this.formatPrice(product.price)}</del> 
               <span class="text-danger fw-bold">${this.formatPrice(product.discount_price)}</span>`
            : `<span class="fw-bold">${this.formatPrice(product.price)}</span>`;

        const imageHTML = product.image
            ? `<img src="${product.image}" class="card-img-top" alt="${product.name}">`
            : `<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 250px;">
                   <i class="fas fa-image fa-3x text-muted"></i>
               </div>`;

        const stockBadge = product.in_stock
            ? '<span class="badge bg-success">Còn hàng</span>'
            : '<span class="badge bg-danger">Hết hàng</span>`;

        return `
            <div class="col-md-4 col-lg-3 mb-4" data-aos="fade-up">
                <div class="card product-card h-100">
                    ${product.is_featured ? '<span class="badge bg-warning position-absolute top-0 start-0 m-2">Nổi bật</span>' : ''}
                    <a href="${product.url}">
                        ${imageHTML}
                    </a>
                    <div class="card-body">
                        <h6 class="card-title">${product.name}</h6>
                        <p class="text-muted small mb-2">${product.brand}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="product-price">${priceHTML}</div>
                            ${stockBadge}
                        </div>
                        <div class="mt-2">
                            ${this.generateStars(product.rating)}
                            <small class="text-muted">(${product.num_reviews})</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderPagination(pagination) {
        const container = document.getElementById('pagination-container');
        if (!container) return;

        if (pagination.total_pages <= 1) {
            container.innerHTML = '';
            return;
        }

        let html = '<nav><ul class="pagination justify-content-center">';

        // Previous button
        html += `
            <li class="page-item ${!pagination.has_prev ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${pagination.page - 1}">Trước</a>
            </li>
        `;

        // Page numbers
        for (let i = 1; i <= pagination.total_pages; i++) {
            if (i === 1 || i === pagination.total_pages ||
                (i >= pagination.page - 2 && i <= pagination.page + 2)) {
                html += `
                    <li class="page-item ${i === pagination.page ? 'active' : ''}">
                        <a class="page-link" href="#" data-page="${i}">${i}</a>
                    </li>
                `;
            } else if (i === pagination.page - 3 || i === pagination.page + 3) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }

        // Next button
        html += `
            <li class="page-item ${!pagination.has_next ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${pagination.page + 1}">Sau</a>
            </li>
        `;

        html += '</ul></nav>';
        container.innerHTML = html;

        // Add click handlers
        container.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(e.target.dataset.page);
                if (page) {
                    this.filters.page = page;
                    this.applyFilters();
                }
            });
        });
    }

    clearFilters() {
        this.filters = {
            category: this.filters.category, // Keep category
            min_price: null,
            max_price: null,
            brands: [],
            scent_types: [],
            tags: [],
            sort: 'name',
            page: 1
        };

        // Reset UI
        document.querySelectorAll('.brand-checkbox, .scent-checkbox').forEach(cb => cb.checked = false);
        document.querySelectorAll('.tag-filter-btn').forEach(btn => btn.classList.remove('active'));

        if (this.priceSlider) {
            this.priceSlider.reset();
        }

        this.applyFilters();
    }

    loadUrlParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.has('category')) this.filters.category = params.get('category');
        if (params.has('min_price')) this.filters.min_price = params.get('min_price');
        if (params.has('max_price')) this.filters.max_price = params.get('max_price');
        if (params.has('sort')) this.filters.sort = params.get('sort');

        this.filters.brands = params.getAll('brand');
        this.filters.scent_types = params.getAll('scent_type');
        this.filters.tags = params.getAll('tag');
    }

    updateUrl(params) {
        const newUrl = `${window.location.pathname}?${params.toString()}`;
        window.history.pushState({}, '', newUrl);
    }

    showLoading() {
        const container = document.getElementById('products-container');
        if (container) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-3">Đang tải sản phẩm...</p>
                </div>
            `;
        }
    }

    hideLoading() {
        // Loading is hidden when products are rendered
    }

    formatPrice(price) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(price);
    }

    generateStars(rating) {
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
}

// Initialize filters on product list page
document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.product-list-page')) {
        window.productFilters = new ProductFilters();
    }
});
