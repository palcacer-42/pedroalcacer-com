// Lightbox functionality for images
document.addEventListener('DOMContentLoaded', function() {
    // Create lightbox modal
    const lightbox = document.createElement('div');
    lightbox.id = 'lightbox';
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img" alt="">
        <div class="lightbox-caption" id="lightbox-caption"></div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeBtn = document.querySelector('.lightbox-close');

    // Function to open lightbox
    function openLightbox(imgSrc, imgAlt) {
        lightbox.style.display = 'flex';
        lightboxImg.src = imgSrc;
        lightboxCaption.textContent = imgAlt;
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }

    // Function to close lightbox
    function closeLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = ''; // Re-enable scrolling
    }

    // Add click event to all images in instrument cards and other content images
    const images = document.querySelectorAll('.instrument-image img, .post-body img');
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            openLightbox(this.src, this.alt);
        });
    });

    // Close lightbox when clicking the close button
    closeBtn.addEventListener('click', closeLightbox);

    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox || e.target === closeBtn) {
            closeLightbox();
        }
    });

    // Close lightbox when pressing ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightbox.style.display === 'flex') {
            closeLightbox();
        }
    });
});
