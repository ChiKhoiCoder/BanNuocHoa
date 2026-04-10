// 3D Viewer Feature
class ThreeDViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.init();
    }
    
    init() {
        console.log('3D Viewer initialized');
        // Three.js initialization would go here
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const viewers = document.querySelectorAll('[data-3d-viewer]');
    viewers.forEach(el => {
        new ThreeDViewer(el.id);
    });
});
