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

// Contact Form Handling
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('contact-email').value;
        const message = document.getElementById('message').value;
        
        // Basic validation
        if (!name.trim() || !email.trim() || !message.trim()) {
            alert('Please fill in all fields.');
            return;
        }
        
        if (!isValidEmail(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        
        // Here you would typically send the message to your backend
        alert('Thank you for your message! I\'ll get back to you within 24 hours.');
        
        // Clear the form
        contactForm.reset();
        
        console.log('Contact form submitted:', { name, email, message });
    });
}

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

// Music Player Placeholder Functions
// These would be replaced with actual music player integration
function playPreview(albumId) {
    console.log(`Playing preview for album ${albumId}`);
    // Here you would integrate with your audio player
    // Could use HTML5 audio, Spotify Web API, SoundCloud Widget, etc.
    alert('Music preview feature coming soon! For now, check out the streaming links.');
}

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

// Add click handlers to album buttons
document.addEventListener('DOMContentLoaded', function() {
    // Listen button handlers
    document.querySelectorAll('.album-card .btn-primary').forEach((button, index) => {
        button.addEventListener('click', () => playPreview(index + 1));
    });
    
    // Buy button handlers
    document.querySelectorAll('.album-card .btn-secondary').forEach((button, index) => {
        button.addEventListener('click', () => purchaseAlbum(index + 1, 10));
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
