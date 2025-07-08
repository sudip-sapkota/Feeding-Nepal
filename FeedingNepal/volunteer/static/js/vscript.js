 // Toggle mobile navigation
 const hamburger = document.getElementById('hamburger');
 const navLinks = document.getElementById('navLinks');

 hamburger.addEventListener('click', () => {
     navLinks.classList.toggle('active');
 });

 // Toggle password visibility
 const passwordField = document.getElementById('password');
 const passwordToggle = document.getElementById('passwordToggle');

 passwordToggle.addEventListener('click', () => {
     if (passwordField.type === 'password') {
         passwordField.type = 'text';
         passwordToggle.textContent = 'Hide';
     } else {
         passwordField.type = 'password';
         passwordToggle.textContent = 'Show';
     }
 });

 // Form validation
 const volunteerForm = document.getElementById('volunteerForm');

 volunteerForm.addEventListener('submit', (e) => {
     e.preventDefault();
     
     // Basic validation
     const password = document.getElementById('password').value;
     if (password.length < 8) {
         alert('Password must be at least 8 characters long');
         return;
     }
     
     // If validation passes, you would normally submit the form
     alert('Form submitted successfully!');
     // volunteerForm.submit(); // Uncomment this in a real application
 });