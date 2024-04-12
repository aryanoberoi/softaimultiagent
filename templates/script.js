document.addEventListener('DOMContentLoaded', function () {
    const contactBtn = document.getElementById('contact-btn');
    const modal = document.getElementById('contact-modal');
    const closeBtn = document.querySelector('.close');

    // Open the modal
    contactBtn.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    // Close the modal
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Close the modal when clicking outside of it
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Form submission
    const form = document.getElementById('contact-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        // Here you can handle form submission, e.g., send data to a server
        alert('Thank you for contacting us!');
        modal.style.display = 'none';
        form.reset();
    });
});
// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));

        window.scrollTo({
            top: target.offsetTop,
            behavior: 'smooth'
        });
    });
});
document.addEventListener('DOMContentLoaded', function () {
    // Existing script content
    // Slider for testimonials
    document.getElementById('next').addEventListener('click', function() {
      const current = document.querySelector('.testimonial.active');
      let next = current.nextElementSibling;
      if (!next) {
        next = document.querySelector('.testimonial:first-child');
      }
      current.classList.remove('active');
      next.classList.add('active');
    });

    // Real-time email validation
    document.getElementById('email').addEventListener('input', function(e) {
      const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
      if (e.target.value.match(emailPattern)) {
        e.target.classList.add('valid');
        e.target.classList.remove('invalid');
      } else {
        e.target.classList.add('invalid');
        e.target.classList.remove('valid');
      }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');
    const logoutLink = document.getElementById('logout-link');

    if (isLoggedIn) {
        // User is logged in
        loginLink.classList.add('hidden');
        signupLink.classList.add('hidden');
        logoutLink.classList.remove('hidden');
    } else {
        // User is logged out
        loginLink.classList.remove('hidden');
        signupLink.classList.remove('hidden');
        logoutLink.classList.add('hidden');
    }

    logoutLink.addEventListener('click', function() {
        // Handle logout
        localStorage.setItem('isLoggedIn', 'false');
        // Toggle visibility
        loginLink.classList.remove('hidden');
        signupLink.classList.remove('hidden');
        logoutLink.classList.add('hidden');
        // Reload or redirect as necessary
        window.location.reload();
    });
});
document.getElementById('logout-button').addEventListener('click', function(event) {
    event.preventDefault(); // Stops the link from navigating
    // Your logout logic here
    console.log('Logging out...');
    // Redirect after logout if necessary
    window.location.href = 'index.html';
});
document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;
    const testimonials = document.querySelectorAll('.testimonial');
    const totalTestimonials = testimonials.length;

    function showTestimonial(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.classList.remove('active');
            if (i === index) {
                testimonial.classList.add('active');
            }
        });
    }

    document.getElementById('next').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % totalTestimonials;
        showTestimonial(currentIndex);
    });

    document.getElementById('prev').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + totalTestimonials) % totalTestimonials;
        showTestimonial(currentIndex);
    });
});

document.getElementById('prev').addEventListener('click', function() {
    console.log('Prev button clicked'); // Debugging line
    currentIndex = (currentIndex - 1 + totalTestimonials) % totalTestimonials;
    showTestimonial(currentIndex);
});
console.log('Current Index:', currentIndex, 'Total Testimonials:', totalTestimonials);
function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
        testimonial.classList.remove('active');
        if (i === index) {
            testimonial.classList.add('active');
        }
    });
}

