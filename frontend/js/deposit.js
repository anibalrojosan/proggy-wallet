$(document).ready(function() {
    // 1. Try to get the user from the local storage
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));

    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Initialize display
    $('#userGreeting').text(`Hello, ${currentUser.username}`);
    updateBalanceDisplay(currentUser.balance);

    function updateBalanceDisplay(amount) {
        $('#currentBalanceDisplay').text(`$${parseFloat(amount).toFixed(2)}`);
    }

    // 3. Handle the deposit form
    $('#depositForm').submit(function(e) {
        e.preventDefault();

        const amountInput = $('#depositAmount').val();
        const amount = parseFloat(amountInput);
        const $message = $('#messageContainer');

        // Validations
        if (isNaN(amount) || amount <= 0) {
            showMessage("Please enter a valid positive amount.", "alert-danger");
            return;
        }

        // Update user data (Simulated in localStorage)
        currentUser.balance += amount;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        // Show success message
        showMessage(`Successfully deposited $${amount.toFixed(2)}!`, "alert-success");
        
        // Update balance display
        $('#currentBalanceDisplay').fadeOut(200, function() {
            updateBalanceDisplay(currentUser.balance);
            $(this).fadeIn(200);
        });

        // Clear form input
        $('#depositAmount').val('');
    });

    // Show message (success or error)
    function showMessage(text, className) {
        const $message = $('#messageContainer');
        $message.text(text)
                .removeClass('d-none alert-danger alert-success')
                .addClass(className)
                .hide()
                .fadeIn();
        
        // If success, hide message after 3 seconds
        if (className === 'alert-success') {
            setTimeout(() => {
                $message.fadeOut(() => $message.addClass('d-none'));
            }, 3000);
        }
    }
});