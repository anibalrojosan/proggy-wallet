$(document).ready(function() {
    // Listen when the form is submitted
    $('#loginForm').on('submit', function(event) {
        // Prevent the page from its default behavior of reloading
        event.preventDefault();

        // Get the values
        const username = $('#username').val().trim();
        const password = $('#password').val().trim();
        const $errorDiv = $('#errorMessage');

        // Basic validation
        if (username === '' || password === '') {
            // Show the Bootstrap error alert message
            $errorDiv.removeClass('d-none');
            return; // Stop the execution
        }

        // If everything is ok, hide the error and simulate success
        $errorDiv.addClass('d-none');
        
        // For now, only redirect to the menu page
        alert('Login successful! Redirecting...');
        window.location.href = 'menu.html';
    });
});