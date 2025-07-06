// Main JavaScript for Wanderlust Travel Guide

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initScrollAnimations();
    initDestinationCards();
    initSmoothScrolling();
    initParallaxEffect();
    initFeatureButtons();
    initAutoDismissMessages();
});

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
        }
    });

    // Close mobile menu when clicking on nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.feature-card, .destination-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Destination cards interaction
function initDestinationCards() {
    const destinationCards = document.querySelectorAll('.destination-card');
    
    destinationCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Parallax effect for hero section
function initParallaxEffect() {
    // Removed floating cards parallax effect
}

// Feature buttons authentication check
function initFeatureButtons() {
    // Check if authentication variables are available
    if (typeof isAuthenticated === 'undefined' || typeof loginUrl === 'undefined') {
        console.warn('Authentication variables not found');
        return;
    }
    
    // Handle hero section buttons
    const featureButtons = document.querySelectorAll('.feature-btn');
    featureButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!isAuthenticated) {
                // Redirect directly to login page
                window.location.href = loginUrl;
            } else {
                // User is authenticated, handle the feature
                const feature = this.getAttribute('data-feature');
                handleFeatureClick(feature);
            }
        });
    });
    
    // Handle feature cards
    const featureCards = document.querySelectorAll('.feature-card-clickable');
    featureCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!isAuthenticated) {
                // Redirect directly to login page
                window.location.href = loginUrl;
            } else {
                // User is authenticated, handle the feature
                const feature = this.getAttribute('data-feature');
                handleFeatureClick(feature);
            }
        });
        
        // Add hover effect to indicate clickability
        card.style.cursor = 'pointer';
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}



// Handle feature clicks for authenticated users
function handleFeatureClick(feature) {
    switch(feature) {
        case 'explore':
            window.location.href = '/explore/';
            break;
        case 'landmark':
            window.location.href = '/find-landmark/';
            break;
        case 'plan':
            window.location.href = '/plan/';
            break;
        default:
            console.log('Unknown feature:', feature);
    }
}

// Auto-dismiss messages after a few seconds
function initAutoDismissMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Check if it's a success or info message (welcome back, logout, etc.)
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            // Auto-dismiss after 4 seconds
            setTimeout(() => {
                // Add fade out effect
                alert.style.transition = 'opacity 0.5s ease-out';
                alert.style.opacity = '0';
                
                // Remove from DOM after fade out
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 4000);
        }
    });
}

// Typing animation for hero text with word cycling
function initTypingAnimation() {
    const gradientSpan = document.querySelector('.text-gradient');
    if (!gradientSpan) return;
    
    const words = ['‎ Vibe', '‎ Scene', '‎ Trip', '‎ Adventure'];
    let currentWordIndex = 0;
    let currentCharIndex = 0;
    let isDeleting = false;
    
    function typeWriter() {
        const currentWord = words[currentWordIndex];
        
        if (isDeleting) {
            // Delete characters
            gradientSpan.textContent = currentWord.substring(0, currentCharIndex - 1);
            currentCharIndex--;
        } else {
            // Type characters
            gradientSpan.textContent = currentWord.substring(0, currentCharIndex + 1);
            currentCharIndex++;
        }
        
        let typeSpeed = 150; // Speed for typing
        
        if (isDeleting) {
            typeSpeed = 100; // Faster deletion
        }
        
        if (!isDeleting && currentCharIndex === currentWord.length) {
            // Pause at end of word
            typeSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && currentCharIndex === 1) {
            // Move to next word
            isDeleting = false;
            currentWordIndex = (currentWordIndex + 1) % words.length;
            typeSpeed = 500; // Pause before next word
        }
        
        setTimeout(typeWriter, typeSpeed);
    }
    
    // Start the animation
    typeWriter();
}

// Counter animation for statistics
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}

// Search functionality (placeholder)
function initSearch() {
    const searchBtn = document.querySelector('.btn-primary');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            // Add search functionality here
            console.log('Search functionality to be implemented');
        });
    }
}

// Video modal functionality
function initVideoModal() {
    const videoBtn = document.querySelector('.btn-outline-light');
    if (videoBtn) {
        videoBtn.addEventListener('click', function() {
            // Add video modal functionality here
            console.log('Video modal to be implemented');
        });
    }
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', function() {
    initTypingAnimation();
    initSearch();
    initVideoModal();
    
    // Add loading animation
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 500);
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized scroll handler
const optimizedScrollHandler = debounce(function() {
    // Handle scroll events efficiently
}, 16);

window.addEventListener('scroll', optimizedScrollHandler);

// Add some interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to feature icons
    const featureIcons = document.querySelectorAll('.feature-icon');
    featureIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
    
    // Add click effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}); 