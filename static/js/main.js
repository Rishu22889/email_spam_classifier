// ===== DOM Elements =====
const emailText = document.getElementById('emailText');
const classifyBtn = document.getElementById('classifyBtn');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const resultIcon = document.getElementById('resultIcon');
const resultTitle = document.getElementById('resultTitle');
const resultBadge = document.getElementById('resultBadge');
const resultConfidence = document.getElementById('resultConfidence');

// ===== Event Listeners =====
classifyBtn.addEventListener('click', classifyEmail);

// Allow Enter key to submit (with Ctrl/Cmd)
emailText.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        classifyEmail();
    }
});

/**
 * Main function to classify email
 */
async function classifyEmail() {
    const text = emailText.value.trim();
    
    // Validation
    if (!text) {
        showError('Please enter email content to classify');
        return;
    }
    
    if (text.length < 10) {
        showError('Email content is too short. Please provide more text for accurate classification.');
        return;
    }
    
    // Hide result section and show loading
    hideResult();
    showLoading();
    
    try {
        // Send POST request to Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_text: text
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Classification failed');
        }
        
        // Hide loading and show result
        hideLoading();
        displayResult(data.prediction, data.confidence);
        
    } catch (error) {
        hideLoading();
        showError('Error: ' + error.message);
    }
}

/**
 * Display classification result with animations
 */
function displayResult(prediction, confidence) {
    const isScam = prediction === 'Scam';

    // Elements
    const resultSection = document.getElementById('result-section');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultBadge = document.getElementById('result-badge');
    const resultConfidence = document.getElementById('result-confidence');

    // Update icon
    resultIcon.className = isScam ? 'fas fa-exclamation-triangle' : 'fas fa-check-circle';
    resultIcon.classList.add(isScam ? 'scam' : 'safe');

    // Update title
    resultTitle.textContent = 'Classification Result';

    // Update badge
    resultBadge.textContent = prediction;
    resultBadge.className = 'result-badge ' + (isScam ? 'scam' : 'safe');

    // Update confidence
    const confidencePercent = (confidence * 100).toFixed(1);
    resultConfidence.innerHTML = `
        <i class="fas fa-chart-line me-2"></i>
        Confidence: <strong>${confidencePercent}%</strong>
    `;

    // Show result section with fade-in animation
    resultSection.style.display = 'block';
    resultSection.classList.remove('animate__fadeIn'); // reset
    void resultSection.offsetWidth; // trigger reflow
    resultSection.classList.add('animate__fadeIn');

    // Add glow effect
    resultSection.style.boxShadow = isScam
        ? '0 0 30px rgba(220, 53, 69, 0.3)'
        : '0 0 30px rgba(40, 167, 69, 0.3)';

    // Scroll to result smoothly
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}


/**
 * Show loading animation
 */
function showLoading() {
    classifyBtn.disabled = true;
    classifyBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    loadingSection.style.display = 'block';
    loadingSection.classList.add('animate__animated', 'animate__fadeIn');
}

/**
 * Hide loading animation
 */
function hideLoading() {
    classifyBtn.disabled = false;
    classifyBtn.innerHTML = '<i class="fas fa-search me-2"></i>Classify Email';
    loadingSection.style.display = 'none';
}

/**
 * Hide result section
 */
function hideResult() {
    resultSection.style.display = 'none';
    resultSection.style.boxShadow = 'none';
    // Remove animation classes
    resultSection.classList.remove('animate__animated', 'animate__fadeIn');
}

/**
 * Show error message with animation
 */
function showError(message) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-danger');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show animate__animated animate__shakeX';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert before the email textarea
    const cardBody = document.querySelector('.main-card .card-body');
    const emailLabel = document.querySelector('label[for="emailText"]');
    cardBody.insertBefore(alertDiv, emailLabel);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
    
    // Scroll to alert
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Add smooth scroll for navigation links
 */
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

/**
 * Add floating navbar on scroll
 */
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll && currentScroll > 80) {
        // Scrolling down
        navbar.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        navbar.style.transform = 'translateY(0)';
    }
    
    lastScroll = currentScroll;
});

// Add transition to navbar
navbar.style.transition = 'transform 0.3s ease';

/**
 * Initialize animations on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Add staggered animation to feature boxes
    const featureBoxes = document.querySelectorAll('.feature-box');
    featureBoxes.forEach((box, index) => {
        box.style.opacity = '0';
        box.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            box.style.transition = 'all 0.5s ease';
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, 100 * index);
    });
    
    // Add focus effect to textarea
    emailText.addEventListener('focus', () => {
        emailText.parentElement.style.transform = 'scale(1.01)';
        emailText.parentElement.style.transition = 'transform 0.3s ease';
    });
    
    emailText.addEventListener('blur', () => {
        emailText.parentElement.style.transform = 'scale(1)';
    });
});

/**
 * Add particle effect on button click (optional enhancement)
 */
classifyBtn.addEventListener('click', (e) => {
    // Create ripple effect
    const ripple = document.createElement('span');
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255, 255, 255, 0.6)';
    ripple.style.width = '100px';
    ripple.style.height = '100px';
    ripple.style.left = e.offsetX - 50 + 'px';
    ripple.style.top = e.offsetY - 50 + 'px';
    ripple.style.animation = 'ripple 0.6s ease-out';
    ripple.style.pointerEvents = 'none';
    
    classifyBtn.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
});

// Add ripple animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * Add sample email on button click (for testing)
 */
function loadSampleScamEmail() {
    emailText.value = `Dear Valued Customer,

URGENT ACTION REQUIRED!

Your account has been suspended due to unusual activity. We need you to verify your identity immediately to avoid permanent account closure.

Click here to confirm your details: http://suspicious-link.com/verify

You have won $10,000 in our lottery! Claim your prize now by providing your bank account details.

This is a limited time offer. Act now or lose access forever!

Regards,
Security Team`;
}

function loadSampleSafeEmail() {
    emailText.value = `Hi there,

Thank you for your recent purchase from our store. Your order #12345 has been confirmed and will be shipped within 2-3 business days.

You can track your order using the link in your account dashboard.

If you have any questions, feel free to reply to this email.

Best regards,
Customer Service Team`;
}

// Add keyboard shortcuts (optional)
document.addEventListener('keydown', (e) => {
    // Ctrl+K or Cmd+K to focus on textarea
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        emailText.focus();
    }
    
    // Escape key to clear textarea
    if (e.key === 'Escape' && document.activeElement === emailText) {
        emailText.value = '';
        hideResult();
    }
});

/**
 * Auto-resize textarea based on content
 */
emailText.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

/**
 * Add character counter (optional)
 */
emailText.addEventListener('input', function() {
    const charCount = this.value.length;
    const formText = this.nextElementSibling;
    
    if (charCount > 0) {
        formText.innerHTML = `
            <i class="fas fa-info-circle"></i> 
            ${charCount} characters | Paste the complete email content for best results
        `;
    } else {
        formText.innerHTML = `
            <i class="fas fa-info-circle"></i> 
            Paste the complete email content for best results
        `;
    }
});

console.log('🚀 Email Scam Classifier loaded successfully!');
console.log('💡 Tip: Press Ctrl+K to focus on the textarea');
console.log('💡 Tip: Press Ctrl+Enter to classify the email');
