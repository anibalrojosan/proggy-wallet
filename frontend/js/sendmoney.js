$(document).ready(function() {
    // 1. Try to get the user from the local storage
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Mock data for contacts
    const contacts = [
        { username: 'maria_perez', name: 'Maria Perez' },
        { username: 'juan_gomez', name: 'Juan Gomez' },
        { username: 'lucia_suarez', name: 'Lucia Suarez' },
        { username: 'admin', name: 'System Admin' }
    ];

    // 3. Initialize interface
    $('#userGreeting').text(`Hello, ${currentUser.username}`);
    updateBalanceDisplay(currentUser.balance);
    loadContacts();

    function updateBalanceDisplay(amount) {
        $('#currentBalanceDisplay').text(`$${parseFloat(amount).toFixed(2)}`);
    }

    function loadContacts() {
        const $select = $('#recipientSelect');
        contacts.forEach(contact => {
            // Don't show the current user in the contact list
            if (contact.username !== currentUser.username) {
                $select.append(`<option value="${contact.username}">${contact.name} (@${contact.username})</option>`);
            }
        });
    }

    // 4. Handle the transfer form
    $('#transferForm').submit(function(e) {
        e.preventDefault();

        const amount = parseFloat($('#transferAmount').val());
        const recipient = $('#recipientSelect').val();
        
        // Validations
        if (!recipient) {
            showMessage("Please select a recipient.", "alert-danger");
            return;
        }

        if (isNaN(amount) || amount <= 0) {
            showMessage("Please enter a valid positive amount.", "alert-danger");
            return;
        }

        // Critical validation: Enough balance
        if (amount > currentUser.balance) {
            showMessage("Insufficient funds. Please enter a lower amount.", "alert-danger");
            return;
        }

        // Confirmation before sending (show a modal with the confirmation)
        if (!confirm(`Are you sure you want to send $${amount.toFixed(2)} to ${recipient}?`)) {
            return;
        }

        // Process transfer (Simulated)
        currentUser.balance -= amount;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        // Show success message
        showMessage(`Successfully sent $${amount.toFixed(2)} to ${recipient}!`, "alert-success");
        
        // Update balance with animation
        $('#currentBalanceDisplay').fadeOut(200, function() {
            updateBalanceDisplay(currentUser.balance);
            $(this).fadeIn(200);
        });

        // Clear form inputs
        $('#transferAmount').val('');
        $('#recipientSelect').val('');
    });

    // Reusable function for messages (same as in deposit.js)
    function showMessage(text, className) {
        const $message = $('#messageContainer');
        $message.text(text)
                .removeClass('d-none alert-danger alert-success')
                .addClass(className)
                .hide()
                .fadeIn();
        
        if (className === 'alert-success') {
            setTimeout(() => {
                $message.fadeOut(() => $message.addClass('d-none'));
            }, 3000);
        }
    }
});