const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');
const visibilityOnIcon = document.getElementById('visibilityOnIcon');
const visibilityOffIcon = document.getElementById('visibilityOffIcon');

// Function to toggle password visibility
function togglePasswordVisibility() {
    // Check the type of the password input
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);

    // Adjust class based on the type
    if (type === 'text') {
        password.classList.remove('password-hidden');
    } else {
        password.classList.add('password-hidden');
    }

    // Toggle the icons
    visibilityOnIcon.style.display = type == 'text' ? 'none' : 'block';
    visibilityOffIcon.style.display = type === 'text' ? 'block' : 'none';
}

// Listen for click events on the toggle button
togglePassword.addEventListener('click', togglePasswordVisibility);

// Listen for keydown events on the toggle button
togglePassword.addEventListener('keydown', function (event) {
    // Check if Enter or Spacebar was pressed
    if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
        event.preventDefault(); // Prevent the default action
        togglePasswordVisibility();
    }
});