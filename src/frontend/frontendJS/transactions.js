// Handle account selection change
document.getElementById('accountSelect').addEventListener('change', function() {
    const account = this.value;
    const addTransactionBtn = document.getElementById('addTransactionBtn');

    // Show the "Add Transaction" button only when an account is selected
    addTransactionBtn.style.display = account ? 'block' : 'none';
});

// Function to toggle the transaction form visibility
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

    // Append the transaction to the table in the right column
    const table = document.getElementById('transactionDetailsTable');
    const newRow = table.insertRow();
    newRow.innerHTML = `<td>${date}</td><td>$${amount}</td><td>${payTo}</td><td>${status}</td>`; 

    // Reset form and hide it after submission
    document.getElementById('transactionFormElement').reset();
    toggleTransactionForm();
}

// Function to add class for dropdown color change
function setDropdownClass(className) {
    document.getElementById('accountSelect').classList.add(className);
}

// Change dropdown background to brown when clicked, revert to green after a delay
function changeDropdownColor() {
    const accountSelect = document.getElementById('accountSelect');
    accountSelect.style.backgroundColor = '#745916'; // Brown color after selection

    // Revert the background color to green after a short delay
    setTimeout(() => {
        accountSelect.style.backgroundColor = '#87991D'; // Green background after selection
    }); // Delay 500ms
}

// Event listener for opening the dropdown when clicked
document.getElementById('accountSelect').addEventListener('click', function() {
    setDropdownClass('open'); // Apply the brown color when clicked
});

// Open popup (Example placeholder function)
function openPopup() {
    alert("Popup logic here");
}
