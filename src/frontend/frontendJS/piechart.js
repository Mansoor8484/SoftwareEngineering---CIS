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
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
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