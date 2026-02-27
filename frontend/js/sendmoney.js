$(document).ready(async function() {
    // 1. Try to get the user from the local storage
    const username = localStorage.getItem('currentUser');
    
    if (!username) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Initialize interface
    $('#userGreeting').text(`Hello, ${username}`);
    await refreshBalance();

    // Initial load: Balance and Contacts
    await Promise.all([
        refreshBalance(),
        loadContacts()
    ]);

    async function refreshBalance() {
        try {
            const response = await fetch(`http://localhost:8000/wallet/status/${username}`);
            const data = await response.json();
            if (response.ok) {
                $('#currentBalanceDisplay').text(`$${data.balance.toFixed(2)}`);
                return data.balance;
            }
        } catch (error) {
            console.error("Error refreshing balance:", error);
        }
        return 0;
    }

    async function loadContacts() {
        const $select = $('#recipientSelect');
        $select.empty().append('<option value="">Choose a recipient...</option>');
        
        try {
            // New endpoint that returns all registered users
            const response = await fetch(`http://localhost:8000/wallet/contacts/${username}`);
            const data = await response.json();
            
            if (response.ok && data.contacts) {
                data.contacts.forEach(contactName => {
                    // Don't show the current user in the list
                    if (contactName !== username) {
                        $select.append(`<option value="${contactName}">${contactName}</option>`);
                    }
                });
            } else {
                console.error("Failed to load contacts:", data.detail);
            }
        } catch (error) {
            console.error("Connection error loading contacts:", error);
            showMessage("Error loading contacts from server", "alert-danger");
        }
    }

    // 3. Handle the transfer form
    $('#transferForm').submit(async function(e) {
        e.preventDefault();

        const amount = parseFloat($('#transferAmount').val());
        const recipient = $('#recipientSelect').val();
        
        if (!recipient || isNaN(amount) || amount <= 0) {
            showMessage("Please fill all fields correctly.", "alert-danger");
            return;
        }

        if (!confirm(`Send $${amount.toFixed(2)} to ${recipient}?`)) return;

        try {
            // Call to the backend
            const response = await fetch('http://localhost:8000/wallet/transfer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    from_user: username, 
                    to_user: recipient, 
                    amount: amount 
                })
            });

            const result = await response.json();

            if (response.ok) {
                showMessage(`Successfully sent $${amount.toFixed(2)}!`, "alert-success");
                
                // Update balance using the transction object returned by the API
                $('#currentBalanceDisplay').fadeOut(200, function() {
                    $(this).text(`$${parseFloat(result.transaction.balance).toFixed(2)}`).fadeIn(200);
                });

                // Clear form
                $('#transferAmount').val('');
                $('#recipientSelect').val('');
            } else {
                // Show business logic error (e.g. insufficient funds)
                showMessage(result.detail || "Transfer failed", "alert-danger");
            }
        } catch (error) {
            console.error("Error sending transfer:", error);
            showMessage("Connection error with server", "alert-danger");
        }
    });

    // Helper: Show messages (success or error)
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