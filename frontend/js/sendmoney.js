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

    // Later, we will get the contacts from the backend
    const contacts = [
        { username: 'user2', name: 'User 2' },
        { username: 'admin', name: 'System Admin' }
    ];
    loadContacts();

    async function refreshBalance() {
        const response = await fetch(`http://localhost:8000/wallet/status/${username}`);
        const data = await response.json();
        if (response.ok) {
            $('#currentBalanceDisplay').text(`$${data.balance.toFixed(2)}`);
            return data.balance;
        }
        return 0;
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
                
                // Update the balance with the real data that the transfer returns
                // transaction.balance is the new balance after the transfer (.transfer() returns transfer_out (transactions of sender))
                $('#currentBalanceDisplay').fadeOut(200, function() {
                    $(this).text(`$${parseFloat(result.transaction.balance).toFixed(2)}`).fadeIn(200);
                });
                $('#transferAmount').val('');
                $('#recipientSelect').val('');
            } else {
                // Here we capture the error of "Insufficient balance" that we sent from the backend
                showMessage(result.detail || "Transfer failed", "alert-danger");
            }
        } catch (error) {
            showMessage("Connection error", "alert-danger");
        }
    });

    // Show messages (same function as in deposit.js)
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