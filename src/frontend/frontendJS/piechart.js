document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        editable: true,
        selectable: true,
        events: [
            { title: 'Groceries', date: '2024-12-05' },
            { title: 'Entertainment', date: '2024-12-10' }
        ],
        dateClick: function(info) {
            var eventTitle = prompt("Enter event title:");
            if (eventTitle) {
                calendar.addEvent({
                    title: eventTitle,
                    start: info.dateStr
                });
            }
        }
    });
    calendar.render();
});


var ctx = document.getElementById('pieChart').getContext('2d');
var pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Groceries', 'Entertainment', 'Utilities', 'Savings'],
        datasets: [{
            label: 'Budget Categories',
            data: [200, 150, 100, 50],
            backgroundColor: ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99'],
            borderColor: '#fff',
            borderWidth: 1
        }]
    }
});


document.getElementById('categoryFilter').addEventListener('change', function(event) {
    var filterValue = event.target.value;
    var newData = [0, 0, 0, 0];
    

    if (filterValue === 'groceries') {
        newData = [200, 0, 0, 0];
    } else if (filterValue === 'entertainment') {
        newData = [0, 150, 0, 0];
    } else if (filterValue === 'utilities') {
        newData = [0, 0, 100, 0];
    } else if (filterValue === 'savings') {
        newData = [0, 0, 0, 50];
    } else {
        newData = [200, 150, 100, 50]; // Show all
    }

    pieChart.data.datasets[0].data = newData;
    pieChart.update();
});

