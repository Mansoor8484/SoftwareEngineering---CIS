
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let currentMonth = date.getMonth(); // Current month (0-11)
    let currentYear = date.getFullYear(); // Current year (e.g. 2024)

    // Update calendar display
    function updateCalendar() {
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        const lastDateOfMonth = new Date(currentYear, currentMonth + 1, 0);
        const lastDayOfMonth = lastDateOfMonth.getDay(); // Get day of the week (0-Sunday, 6-Saturday)
        const lastDate = lastDateOfMonth.getDate(); // Get last date of the month (e.g., 30 or 31)

        // Update the month-year display
        document.getElementById("monthYear").innerText = `${monthNames[currentMonth]} ${currentYear}`;

        // Create the calendar table body
        const tableBody = document.getElementById("calendarTable").getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ""; // Clear the previous month's days

        // Generate empty cells for the first week
        let row = document.createElement("tr");
        for (let i = 0; i < firstDayOfMonth.getDay(); i++) {
            const cell = document.createElement("td");
            row.appendChild(cell);
        }

        // Fill the days of the month
        for (let day = 1; day <= lastDate; day++) {
            const cell = document.createElement("td");
            cell.innerText = day;
            cell.addEventListener("click", () => alert(`Viewing ${monthNames[currentMonth]} ${day}, ${currentYear}`));
            row.appendChild(cell);

            // If it's the end of the week, create a new row
            if (row.children.length === 7) {
                tableBody.appendChild(row);
                row = document.createElement("tr");
            }
        }

        // Add the last row if needed
        if (row.children.length > 0) {
            tableBody.appendChild(row);
        }
    }

    // Navigation to previous month
    document.getElementById("prevMonth").addEventListener("click", () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        updateCalendar();
    });

    // Navigation to next month
    document.getElementById("nextMonth").addEventListener("click", () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar();
    });

    // Initialize the calendar
    updateCalendar();
