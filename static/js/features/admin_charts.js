// Admin Charts Feature
document.addEventListener('DOMContentLoaded', function() {
    // Chart.js initialization for admin dashboard
    const chartElements = document.querySelectorAll('[data-chart]');
    
    chartElements.forEach(el => {
        const ctx = el.getContext('2d');
        const chartType = el.dataset.chart;
        
        // Chart will be initialized by dashboard-specific code
        console.log(`Chart element found: ${chartType}`);
    });
});
