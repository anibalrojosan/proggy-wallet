$(document).ready(function() {
    // Listen when the form is submitted
    $('#loginForm').on('submit', async function(event) {
        // Prevent the page from its default behavior of reloading
        event.preventDefault();

        // Get the values
        const username = $('#username').val().trim();
        const password = $('#password').val().trim();
        const $errorDiv = $('#errorMessage');

        // Basic validation
        if (username === '' || password === '') {
            // Show the Bootstrap error alert message
            $errorDiv.text('Please fill in all fields.').removeClass('d-none');
            return; // Stop the execution
        }

        try {
            // Call to the backend API
            const response = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();

            if (response.ok) {
                // SUCCESS: We only save the username in localStorage to identify the session
                localStorage.setItem('currentUser', result.user.username);
                
                $errorDiv.addClass('d-none');
                alert('Welcome ' + result.user.username + '! Redirecting...');
                window.location.href = 'menu.html';
            } else {
                // ERROR: Show the message that comes from the backend (HTTPException)
                $errorDiv.text(result.detail || "Invalid credentials").removeClass('d-none');
            }
        } catch (error) {
            // Connection error: The server is down or there are network problems
            console.error('Connection error:', error);
            $errorDiv.text("Cannot connect to server. Is the backend running?").removeClass('d-none');
        }
    });
});