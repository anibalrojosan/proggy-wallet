$(document).ready(function() {
    // Try to get the user from the local storage
    const user = JSON.parse(localStorage.getItem('currentUser'));

    // Security: If there is no user, send him back to the login
    if (!user) {
        window.location.href = 'login.html';
        return;
    }

    // Update the interface
    $('#welcomeMessage').text(`Welcome, ${user.username}!`);
    
    // Also update the balance
    $('#balanceDisplay').text(`$${user.balance.toFixed(2)}`);

    // Logout button logic
    $('#btnLogout').click(function() {
        localStorage.removeItem('currentUser');
        window.location.href = 'login.html';
    });
});