// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Email Form Handling
const emailForm = document.getElementById('emailForm');
if (emailForm) {
    emailForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        
        // Basic email validation
        if (!isValidEmail(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        
        // Here you would typically send the email to your backend service
        // For now, we'll just show a success message
        alert('Thank you for joining our mailing list! You\'ll receive exclusive content soon.');
        
        // Clear the form
        document.getElementById('email').value = '';
        
        // In a real implementation, you might redirect to a thank you page
        // or update the UI to show success state
        
        console.log('Email submitted:', email);
        
        // Example of how you might send this to a service like Netlify Forms
        // or integrate with Mailchimp, ConvertKit, etc.
        /*
        fetch('/', {
            method: 'POST',
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                'form-name': 'email-signup',
                'email': email
            }).toString()
        }).then(() => {
            alert('Thank you for subscribing!');
        }).catch(() => {
            alert('Error submitting form. Please try again.');
        });
        */
    });
}

// Email Signup Form Handling (Main Page)
const emailSignupForm = document.getElementById('emailSignupForm');
if (emailSignupForm) {
    let signupCooldown = false;
    emailSignupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (signupCooldown) {
            alert('You have already signed up.');
            return;
        }
        // Honeypot check - if filled, it's a bot
        const honeypot = document.getElementById('website');
        if (honeypot && honeypot.value.trim() !== '') {
            // Silently reject bots - don't give them any feedback
            console.log('Bot detected via honeypot');
            return;
        }
        const email = document.getElementById('signup-email').value;
        // Block suspicious email domains
        const suspiciousDomains = ['banlamail.com', '10minutemail.com', 'guerrillamail.com', 'tempmail.org'];
        const emailDomain = email.split('@')[1]?.toLowerCase();
        if (suspiciousDomains.includes(emailDomain)) {
            alert('Please use a permanent email address.');
            return;
        }
        // Basic email validation
        if (!isValidEmail(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        // Send signup email via EmailJS (use business service)
        emailjs.send("service_4zxwjam", "template_tx4flvd", {
            to_email: email,
            album_name: "Mailing List Signup",
            download_link: "Welcome to Elemental Publishing!",
            customer_name: "New Subscriber"
        }).then(function(response) {
            console.log('Signup email sent successfully:', response);
            // Track email signup conversion
            if (typeof gtag !== 'undefined') {
                trackEmailSignup('main_page');
            }
            alert('🎵 Welcome to the list! Check your email for exclusive content.');
            document.getElementById('signup-email').value = '';
            signupCooldown = true;
            setTimeout(function() {
                signupCooldown = false;
            }, 30000); // 30 seconds
        }, function(error) {
            console.log('Signup email failed:', error);
            // Still track the signup attempt
            if (typeof gtag !== 'undefined') {
                trackEmailSignup('main_page');
            }
            alert('Thanks for signing up! You\'re on the list.');
            document.getElementById('signup-email').value = '';
            signupCooldown = true;
            setTimeout(function() {
                signupCooldown = false;
            }, 30000); // 30 seconds
        });
    });
}

// ...existing code...

// Email validation helper function
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in class to elements that should animate
    const animatedElements = document.querySelectorAll('.album-card, .stat, .about-text, .contact-info');
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
});

// SoundCloud Album Data
const albumData = {
    'type-1': {
        key: 'type1',
        title: 'Type 1',
        soundcloudUrl: 'https://soundcloud.com/elementalpublishing/sets/spiderfox-type-one', // Replace with actual URL
        embedUrl: 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1789617261&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true'
    },
    'strip-tape': {
        key: 'striptape',
        title: 'Strip Tape',
        soundcloudUrl: 'https://soundcloud.com/elementalpublishing/sets/strip-tape', // Replace with actual URL
        embedUrl: 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1806004999&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true'
    },
    'new-matrix': {
        key: 'newmatrix',
        title: 'New Matrix',
        soundcloudUrl: 'https://soundcloud.com/elementalpublishing/sets/new-matrix', // Replace with actual URL
        embedUrl: 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1848997065&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true'
    }
};

// Create and show SoundCloud player modal
function showAlbumPreview(albumKey) {
    const album = albumData[albumKey];
    if (!album) {
        console.error('Album not found:', albumKey);
        return;
    }

    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'preview-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Preview: ${album.title}</h3>
                <button class="close-modal" onclick="closePreviewModal()">&times;</button>
            </div>
            <div class="modal-body">
                <iframe 
                    width="100%" 
                    height="300" 
                    scrolling="no" 
                    frameborder="no" 
                    allow="autoplay" 
                    src="${album.embedUrl}">
                </iframe>
                <div class="modal-actions">
                    <a href="${album.soundcloudUrl}" target="_blank" class="btn btn-primary">
                        Full Playlist on SoundCloud
                    </a>
                    <button class="btn btn-secondary" onclick="closePreviewModal(); buyAlbumFromModal('${album.key}')">
                        Buy Direct - $15
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

// Close preview modal
function closePreviewModal() {
    const modal = document.querySelector('.preview-modal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    }
}

// Handle escape key to close modal
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePreviewModal();
    }
});

// Click outside modal to close
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('preview-modal')) {
        closePreviewModal();
    }
});

function purchaseAlbum(albumId, price) {
    console.log(`Purchasing album ${albumId} for $${price}`);
    // Here you would integrate with PayPal, Stripe, or other payment processor
    
    // Example PayPal integration would look like this:
    /*
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: price
                    },
                    description: `Album ${albumId} - Digital Download`
                }]
            });
        },
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                alert('Payment successful! Download link will be sent to your email.');
                // Redirect to download page or send download link
            });
        }
    }).render('#paypal-button-container');
    */
    
    alert(`Purchase feature coming soon! Album would cost $${price}. You'll receive download links immediately after payment.`);
}

// Buy album from modal (connects to main page PayPal integration)
function buyAlbumFromModal(albumKey) {
    // Use the buyAlbum function from index.html if available
    if (typeof buyAlbum === 'function') {
        buyAlbum(albumKey);
    } else {
        // Fallback: redirect to main page and scroll to album
        window.location.href = `index.html#music`;
    }
}

// Add click handlers to album buttons
document.addEventListener('DOMContentLoaded', function() {
    // Preview button handlers - updated to use album keys
    const previewButtons = document.querySelectorAll('.album-card .btn-primary');
    const albumKeys = ['type-1', 'strip-tape', 'new-matrix'];
    
    previewButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            if (albumKeys[index]) {
                showAlbumPreview(albumKeys[index]);
            }
        });
    });
    
    // Buy button handlers remain the same since they're now direct PayPal links
    document.querySelectorAll('.album-card .btn-secondary').forEach((button, index) => {
        // These are now handled by direct PayPal links in HTML
        console.log(`Buy button ${index + 1} ready (handled by PayPal link)`);
    });
});

// Navigation highlight on scroll
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Performance optimization: Lazy load images when implemented
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading when DOM is ready
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Console message for developers
console.log(`
🎵 Elemental Publishing Website
Built for independent artists who want to own their fan relationships.
No platform fees. No algorithms. Direct artist-to-fan connection.

This site is optimized for:
- Direct music sales
- Email list building  
- Social media traffic conversion
- Mobile-first experience
- Fast loading and SEO

Ready to customize for your music business!
`);
