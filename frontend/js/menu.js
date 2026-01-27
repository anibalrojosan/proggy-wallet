$(document).ready(async function() {
    // Try to get the user from the local storage
    const username = localStorage.getItem('currentUser');

    // Security: If there is no user, send him back to the login
    if (!username) {
        window.location.href = 'login.html';
        return;
    }

    try {
        // Request the real wallet status to the backend
        const response = await fetch(`http://localhost:8000/wallet/status/${username}`);
        const data = await response.json();

        if (response.ok) {
            // Update the interface with the real data from the server
            $('#welcomeMessage').text(`Welcome, ${data.username}!`);
            $('#balanceDisplay').text(`$${data.balance.toFixed(2)}`);
            
            // Optional: show how many transactions the user has
            console.log(`User has ${data.history_count} transactions.`);
        } else {
            // If the user does not exist in the backend but was in localStorage, remove the user from the localStorage
            localStorage.removeItem('currentUser');
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        $('#balanceDisplay').text("Error loading balance");
    }

    // Logout button logic
    $('#btnLogout').click(function() {
        localStorage.removeItem('currentUser');
        window.location.href = 'login.html';
    });
});