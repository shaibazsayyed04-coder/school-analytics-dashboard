const ctx = document.getElementById('attendanceChart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Std 1', 'Std 2', 'Std 3'],
        datasets: [{
            label: 'Attendance %',
            data: [80, 72, 90]
        }]
    }
});
