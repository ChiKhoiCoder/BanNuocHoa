// View Count Feature
document.addEventListener('DOMContentLoaded', function() {
    // Track page views
    const productId = document.body.dataset.productId;
    if (productId) {
        fetch(`/api/product/${productId}/view/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
            }
        }).catch(err => console.log('View tracking not available'));
    }
});
