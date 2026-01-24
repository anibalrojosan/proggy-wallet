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
        
        // Simulate user data
        const userData = {
            username: username,
            balance: 1500.50, // Simulate balance
            email: username.toLowerCase() + "@wallet.com"
        };
        
        // Store the user data in the local storage
        localStorage.setItem('currentUser', JSON.stringify(userData));

        alert('Welcome ' + username + '! Redirecting to the menu...');
        window.location.href = 'menu.html';
    });
});