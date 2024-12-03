// Account selection change
document.getElementById('accountSelect').addEventListener('change', function() {
    const account = this.value;
    const addTransactionBtn = document.getElementById('addTransactionBtn');

    // Reveal "Add Transaction" button
    addTransactionBtn.style.display = account ? 'block' : 'none';
});

// toggle the transaction form visibility
function toggleTransactionForm() {
    const form = document.getElementById('transactionForm');
    form.style.display = form.style.display === 'block' ? 'none' : 'block';
}

// Handle transaction form submission
function submitTransaction() {
    const date = document.getElementById('transactionDate').value;
    const amount = document.getElementById('transactionAmount').value;
    const payTo = document.getElementById('payTo').value;
    const status = document.getElementById('transactionStatus').value;

    // Validate form fields
    if (!date || !amount || !payTo || !status) {
        alert("All fields are required!");
        return;
    }

    // Send transaction to the table
    const table = document.getElementById('transactionDetailsTable');
    const newRow = table.insertRow();
    newRow.innerHTML = `<td>${date}</td><td>$${amount}</td><td>${payTo}</td><td>${status}</td>`; 

    // Reset form and hide form after submission
    document.getElementById('transactionFormElement').reset();
    toggleTransactionForm();
}

// Function to add class for dropdown color change
function setDropdownClass(className) {
    document.getElementById('accountSelect').classList.add(className);
}

// Change dropdown background to brown when clicked
function changeDropdownColor() {
    const accountSelect = document.getElementById('accountSelect');
    accountSelect.style.backgroundColor = '#745916';

    // Revert the background color to green
    setTimeout(() => {
        accountSelect.style.backgroundColor = '#87991D';
    });
}

// Event listener for opening the dropdown
document.getElementById('accountSelect').addEventListener('click', function() {
    setDropdownClass('open');
});

// Open popup
function openPopup() {
    alert("Popup logic here");
}