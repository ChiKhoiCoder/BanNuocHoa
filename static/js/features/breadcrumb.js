// Breadcrumb Navigation Feature
document.addEventListener('DOMContentLoaded', function() {
    // Add active state to breadcrumb current page
    const breadcrumbs = document.querySelectorAll('.breadcrumb-item');
    if (breadcrumbs.length > 0) {
        const lastItem = breadcrumbs[breadcrumbs.length - 1];
        lastItem.classList.add('active');
        lastItem.style.pointerEvents = 'none';
    }
});
