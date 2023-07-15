$(document).ready(function() {
    // Function to refresh data every 10 seconds
    function refreshData() {
        fetch('/update_data')
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Error: ' + response.status);
                }
                return response.json();
            })
            .then(function(data) {
                // Create a new row with the updated data
                var newRow = '<tr>' +
                                '<td>' + data['eplf_payment_data'] + '</td>' +
                                '<td>' + data['zd_payment_data'] + '</td>' +
                                '<td>' + data['eplf_log_data'] + '</td>' +
                                '<td>' + data['zd_log_data'] + '</td>' +
                                '<td>' + getCurrentTime() + '</td>' +
                             '</tr>';

                // Append the new row to the table body
                $('#data-table').append(newRow);
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
    }

    // Run refreshData immediately and then every 1 Minute
    refreshData();
    setInterval(refreshData, 60000);
});

// Function to get the current time in the format HH:MM:SS
function getCurrentTime() {
    var now = new Date();
    var hours = String(now.getHours()).padStart(2, '0');
    var minutes = String(now.getMinutes()).padStart(2, '0');
    var seconds = String(now.getSeconds()).padStart(2, '0');
    return hours + ':' + minutes + ':' + seconds;
}
