$(document).ready(async function() {
    // 1. Get the username from the local storage
    const username = localStorage.getItem('currentUser');
    if (!username) {
        window.location.href = 'login.html';
        return;
    }

    let transactions = [];
    let currentFilter = 'all';
    let sortOrder = 'desc'; // Descending by date by default

    // 2. Function to load data from the backend
    async function loadTransactions() {
        try {
            const response = await fetch(`http://localhost:8000/wallet/history/${username}`);
            const data = await response.json();
            
            if (response.ok) {
                transactions = data.transactions;
                renderTable(); // Render the table after receiving the data
            }
        } catch (error) {
            console.error("Error loading history:", error);
            $('#noTransactions').text("Error connecting to server").removeClass('d-none');
        }
    }

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

                // Get the counterparty (the user that is receiving or sending money)
                const counterparty = (t.type === 'transfer_out') ? t.to_user : t.from_user;

                // DOM insertion (append a new row to the table)
                $body.append(`
                    <tr>
                        <td class="small text-muted">${dateFormatted}</td>
                        <td><i class="bi ${typeIcon} ${typeClass}"></i> ${typeText}</td>
                        <td>${t.counterparty}</td>
                        <td class="fw-bold ${typeClass}">${t.type === 'transfer_out' ? '-' : '+'}$${parseFloat(t.amount).toFixed(2)}</td>
                        <td class="text-muted">$${parseFloat(t.balance).toFixed(2)}</td>
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
    await loadTransactions();
});