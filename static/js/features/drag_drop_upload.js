// Drag Drop Upload Feature
document.addEventListener('DOMContentLoaded', function() {
    const dropzones = document.querySelectorAll('[data-dropzone]');
    
    dropzones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
        
        zone.addEventListener('dragleave', () => {
            zone.classList.remove('dragover');
        });
        
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            console.log(`${files.length} files dropped`);
            // Handle file upload
        });
    });
});
