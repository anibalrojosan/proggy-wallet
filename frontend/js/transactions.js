$(document).ready(function() {
    // 1. Try to get the user from the local storage
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Load transactions (or use example data if empty)
    let transactions = JSON.parse(localStorage.getItem(`transactions_${currentUser.username}`)) || [];

    // If there are no data, add some example data for testing
    if (transactions.length === 0) {
        transactions = [
            { date: '2023-10-25T14:30:00Z', type: 'deposit', counterparty: 'Initial Deposit', amount: 1000.0, balance: 1000.0 },
            { date: '2023-10-26T10:15:00Z', type: 'transfer_out', counterparty: 'maria_perez', amount: 50.0, balance: 950.0 },
            { date: '2023-10-27T12:00:00Z', type: 'transfer_in', counterparty: 'juan_gomez', amount: 20.0, balance: 970.0 }
        ];
        // Save the example data for persistence
        localStorage.setItem(`transactions_${currentUser.username}`, JSON.stringify(transactions));
    }

    let currentFilter = 'all';
    let sortOrder = 'desc'; // Descending by date by default

    // 3. Function to render the table
    function renderTable() {
        const $body = $('#transactionsBody');
        const $noData = $('#noTransactions');
        $body.empty();

        // Apply filters
        let filtered = transactions.filter(t => {
            if (currentFilter === 'income') return t.type === 'deposit' || t.type === 'transfer_in';
            if (currentFilter === 'expenses') return t.type === 'transfer_out';
            return true;
        });

        // Apply sorting
        filtered.sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
        });

        if (filtered.length === 0) {
            $noData.removeClass('d-none');
        } else {
            $noData.addClass('d-none');
            filtered.forEach(t => {
                const dateFormatted = new Date(t.date).toLocaleString();
                const typeClass = (t.type === 'transfer_out') ? 'text-danger' : 'text-success';
                const typeIcon = (t.type === 'transfer_out') ? 'bi-arrow-up-right' : 'bi-arrow-down-left';
                const typeText = t.type === 'deposit' ? 'Deposit' : (t.type === 'transfer_out' ? 'Transfer Out' : 'Transfer In');

                // DOM insertion (append a new row to the table)
                $body.append(`
                    <tr>
                        <td class="small text-muted">${dateFormatted}</td>
                        <td><i class="bi ${typeIcon} ${typeClass}"></i> ${typeText}</td>
                        <td>${t.counterparty}</td>
                        <td class="fw-bold ${typeClass}">${t.type === 'transfer_out' ? '-' : '+'}$${t.amount.toFixed(2)}</td>
                        <td class="text-muted">$${t.balance.toFixed(2)}</td>
                    </tr>
                `);
            });
        }
    }

    // 4. Event handlers (changes currentFilter or sortOrder and calls renderTable function)
    $('#filterAll').click(function() {
        $('.btn-group .btn').removeClass('active');
        $(this).addClass('active');
        currentFilter = 'all';
        renderTable();
    });

    $('#filterIncome').click(function() {
        $('.btn-group .btn').removeClass('active');
        $(this).addClass('active');
        currentFilter = 'income';
        renderTable();
    });

    $('#filterExpenses').click(function() {
        $('.btn-group .btn').removeClass('active');
        $(this).addClass('active');
        currentFilter = 'expenses';
        renderTable();
    });

    // Sort by date when clicking on the header
    $('#sortDate').click(function() {
        sortOrder = (sortOrder === 'desc') ? 'asc' : 'desc';
        renderTable();
    });

    // Initial load
    renderTable();
});