
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let currentMonth = date.getMonth(); 
    let currentYear = date.getFullYear(); 

    // Update calendar
    function updateCalendar() {
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        const lastDateOfMonth = new Date(currentYear, currentMonth + 1, 0);
        const lastDayOfMonth = lastDateOfMonth.getDay(); 
        const lastDate = lastDateOfMonth.getDate(); 

        // Update the month-year display
        document.getElementById("monthYear").innerText = `${monthNames[currentMonth]} ${currentYear}`;

        // Create the calendar
        const tableBody = document.getElementById("calendarTable").getElementsByTagName('tbody')[0];
        tableBody.innerHTML = "";

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

    // Nav to previous month
    document.getElementById("prevMonth").addEventListener("click", () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        updateCalendar();
    });

    // Nav to next month
    document.getElementById("nextMonth").addEventListener("click", () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar();
    });

    // Initialize
    updateCalendar();
