/**
 * Checkout.js - Checkout Progress Bar & Address Autocomplete
 */

document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.checkout-page')) {
        initializeCheckout();
    }
});

/**
 * Initialize checkout functionality
 */
function initializeCheckout() {
    setupProgressBar();
    setupAddressAutocomplete();
    setupFormValidation();
}

/**
 * Setup checkout progress bar
 */
function setupProgressBar() {
    const steps = document.querySelectorAll('.checkout-step');
    const currentStep = getCurrentStep();

    steps.forEach((step, index) => {
        if (index < currentStep) {
            step.classList.add('completed');
        } else if (index === currentStep) {
            step.classList.add('active');
        }
    });
}

/**
 * Get current checkout step
 */
function getCurrentStep() {
    const page = window.location.pathname;

    if (page.includes('cart')) return 0;
    if (page.includes('checkout')) return 1;
    if (page.includes('payment')) return 2;
    if (page.includes('confirmation')) return 3;

    return 1; // Default to checkout step
}

/**
 * Setup address autocomplete with Vietnamese provinces/cities
 */
function setupAddressAutocomplete() {
    const cityInput = document.getElementById('id_city');
    const stateInput = document.getElementById('id_state');
    const addressInput = document.getElementById('id_address');

    if (cityInput) {
        setupCityAutocomplete(cityInput);
    }

    if (stateInput) {
        setupStateAutocomplete(stateInput);
    }

    if (addressInput) {
        setupAddressInput(addressInput);
    }
}

/**
 * Vietnamese cities/provinces data
 */
const vietnameseCities = [
    'Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
    'An Giang', 'Bà Rịa - Vũng Tàu', 'Bắc Giang', 'Bắc Kạn', 'Bạc Liêu',
    'Bắc Ninh', 'Bến Tre', 'Bình Định', 'Bình Dương', 'Bình Phước',
    'Bình Thuận', 'Cà Mau', 'Cao Bằng', 'Đắk Lắk', 'Đắk Nông',
    'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Giang',
    'Hà Nam', 'Hà Tĩnh', 'Hải Dương', 'Hậu Giang', 'Hòa Bình',
    'Hưng Yên', 'Khánh Hòa', 'Kiên Giang', 'Kon Tum', 'Lai Châu',
    'Lâm Đồng', 'Lạng Sơn', 'Lào Cai', 'Long An', 'Nam Định',
    'Nghệ An', 'Ninh Bình', 'Ninh Thuận', 'Phú Thọ', 'Phú Yên',
    'Quảng Bình', 'Quảng Nam', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị',
    'Sóc Trăng', 'Sơn La', 'Tây Ninh', 'Thái Bình', 'Thái Nguyên',
    'Thanh Hóa', 'Thừa Thiên Huế', 'Tiền Giang', 'Trà Vinh', 'Tuyên Quang',
    'Vĩnh Long', 'Vĩnh Phúc', 'Yên Bái'
];

/**
 * Setup city autocomplete
 */
function setupCityAutocomplete(input) {
    const datalist = document.createElement('datalist');
    datalist.id = 'cities-list';

    vietnameseCities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        datalist.appendChild(option);
    });

    document.body.appendChild(datalist);
    input.setAttribute('list', 'cities-list');
    input.setAttribute('autocomplete', 'off');

    // Create custom dropdown
    createCustomDropdown(input, vietnameseCities, 'city');
}

/**
 * Setup state/district autocomplete
 */
function setupStateAutocomplete(input) {
    input.setAttribute('autocomplete', 'off');

    // Listen for city selection to load districts
    const cityInput = document.getElementById('id_city');
    if (cityInput) {
        cityInput.addEventListener('change', function () {
            loadDistricts(this.value, input);
        });
    }
}

/**
 * Load districts based on city
 */
function loadDistricts(city, stateInput) {
    // This would typically fetch from an API
    // For now, we'll use a simple implementation
    const districts = getDistrictsForCity(city);

    if (districts.length > 0) {
        createCustomDropdown(stateInput, districts, 'district');
    }
}

/**
 * Get districts for a city (simplified)
 */
function getDistrictsForCity(city) {
    // This is a simplified version. In production, you'd fetch from an API
    const districtMap = {
        'Hà Nội': ['Ba Đình', 'Hoàn Kiếm', 'Tây Hồ', 'Long Biên', 'Cầu Giấy', 'Đống Đa', 'Hai Bà Trưng', 'Hoàng Mai', 'Thanh Xuân', 'Nam Từ Liêm', 'Bắc Từ Liêm', 'Hà Đông'],
        'Hồ Chí Minh': ['Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Thủ Đức', 'Bình Thạnh', 'Phú Nhuận', 'Tân Bình', 'Tân Phú', 'Gò Vấp'],
        'Đà Nẵng': ['Hải Châu', 'Thanh Khê', 'Sơn Trà', 'Ngũ Hành Sơn', 'Liên Chiểu', 'Cẩm Lệ', 'Hòa Vang']
    };

    return districtMap[city] || [];
}

/**
 * Create custom dropdown for autocomplete
 */
function createCustomDropdown(input, items, type) {
    // Remove existing dropdown
    const existingDropdown = document.getElementById(`${type}-dropdown`);
    if (existingDropdown) {
        existingDropdown.remove();
    }

    const dropdown = document.createElement('div');
    dropdown.id = `${type}-dropdown`;
    dropdown.className = 'autocomplete-dropdown';
    dropdown.style.display = 'none';

    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(dropdown);

    // Input event listener
    input.addEventListener('input', function () {
        const value = this.value.toLowerCase();

        if (value.length < 1) {
            dropdown.style.display = 'none';
            return;
        }

        const filtered = items.filter(item =>
            item.toLowerCase().includes(value)
        );

        if (filtered.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        dropdown.innerHTML = '';
        filtered.slice(0, 10).forEach(item => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.textContent = item;
            div.addEventListener('click', function () {
                input.value = item;
                dropdown.style.display = 'none';
                input.dispatchEvent(new Event('change'));
            });
            dropdown.appendChild(div);
        });

        dropdown.style.display = 'block';
    });

    // Click outside to close
    document.addEventListener('click', function (e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

/**
 * Setup address input with validation
 */
function setupAddressInput(input) {
    input.addEventListener('blur', function () {
        validateAddress(this);
    });
}

/**
 * Validate address
 */
function validateAddress(input) {
    const value = input.value.trim();
    const feedback = input.parentNode.querySelector('.invalid-feedback') || createFeedbackElement(input);

    if (value.length < 10) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = 'Địa chỉ quá ngắn. Vui lòng nhập địa chỉ chi tiết.';
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '';
    }
}

/**
 * Create feedback element
 */
function createFeedbackElement(input) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    input.parentNode.appendChild(feedback);
    return feedback;
}

/**
 * Setup real-time form validation
 */
function setupFormValidation() {
    const form = document.querySelector('.checkout-form');
    if (!form) return;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        // Validate on blur
        input.addEventListener('blur', function () {
            validateField(this);
        });

        // Remove error on input
        input.addEventListener('input', function () {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });

    // Form submit validation
    form.addEventListener('submit', function (e) {
        let isValid = true;

        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();

            // Scroll to first error
            const firstError = form.querySelector('.is-invalid');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }

            // Show notification
            if (typeof notyf !== 'undefined') {
                notyf.error('Vui lòng kiểm tra lại thông tin.');
            }
        }
    });
}

/**
 * Validate individual field
 */
function validateField(input) {
    const value = input.value.trim();
    const type = input.type;
    const name = input.name;
    let isValid = true;
    let message = '';

    // Required check
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Trường này là bắt buộc.';
    }

    // Email validation
    else if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Email không hợp lệ.';
        }
    }

    // Phone validation
    else if (name === 'phone' && value) {
        const phoneRegex = /^[0-9]{10,11}$/;
        if (!phoneRegex.test(value.replace(/\s/g, ''))) {
            isValid = false;
            message = 'Số điện thoại không hợp lệ.';
        }
    }

    // Zip code validation
    else if (name === 'zip_code' && value) {
        const zipRegex = /^[0-9]{5,6}$/;
        if (!zipRegex.test(value)) {
            isValid = false;
            message = 'Mã bưu điện không hợp lệ.';
        }
    }

    // Update UI
    const feedback = input.parentNode.querySelector('.invalid-feedback') || createFeedbackElement(input);

    if (isValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '';
    } else {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        feedback.textContent = message;
    }

    return isValid;
}

/**
 * Move to next step
 */
function nextStep(currentStepNum) {
    const currentStep = document.querySelector(`.step-content[data-step="${currentStepNum}"]`);
    const nextStep = document.querySelector(`.step-content[data-step="${currentStepNum + 1}"]`);

    if (currentStep && nextStep) {
        currentStep.classList.remove('active');
        nextStep.classList.add('active');

        updateProgressBar(currentStepNum + 1);
    }
}

/**
 * Update progress bar
 */
function updateProgressBar(stepNum) {
    const steps = document.querySelectorAll('.checkout-step');

    steps.forEach((step, index) => {
        if (index < stepNum) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (index === stepNum) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
}
