// Radar Chart Feature
document.addEventListener('DOMContentLoaded', function() {
    const radarCharts = document.querySelectorAll('[data-radar-chart]');
    
    radarCharts.forEach(el => {
        if (typeof Chart !== 'undefined') {
            const ctx = el.getContext('2d');
            // Radar chart will be created with configuration from data attributes
            console.log('Radar chart element found');
        }
    });
});
