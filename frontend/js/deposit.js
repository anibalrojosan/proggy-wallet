$(document).ready(async function() {
    // 1. Try to get the user from the local storage
    const username = localStorage.getItem('currentUser');

    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Initialize display loading data from the backend
    $('#userGreeting').text(`Hello, ${username}`);
    await refreshBalance();

    async function refreshBalance() {
        try {
            const response = await fetch(`http://localhost:8000/wallet/status/${username}`);
            const data = await response.json();
            if (response.ok) {
                $('#currentBalanceDisplay').text(`$${data.balance.toFixed(2)}`);
            }
        } catch (error) {
            console.error("Error refreshing balance:", error);
        }
    }

    // 3. Handle the deposit form
    $('#depositForm').submit(async function(e) {
        e.preventDefault();

        const amountInput = $('#depositAmount').val();
        const amount = parseFloat(amountInput);

        // Validations
        if (isNaN(amount) || amount <= 0) {
            showMessage("Please enter a valid positive amount.", "alert-danger");
            return;
        }

        try {
            // Call to the backend
            const response = await fetch('http://localhost:8000/wallet/deposit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, amount })
            });

            const result = await response.json();

            if (response.ok) {
                showMessage(`Successfully deposited $${amount.toFixed(2)}!`, "alert-success");
                
                // Update the balance with animation using the real data from the backend
                $('#currentBalanceDisplay').fadeOut(200, function() {
                    $(this).text(`$${parseFloat(result.transaction.balance).toFixed(2)}`).fadeIn(200);
                });
                $('#depositAmount').val('');
            } else {
                showMessage(result.detail || "Error processing deposit", "alert-danger");
            }
        } catch (error) {
            showMessage("Connection error with backend", "alert-danger");
        }
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