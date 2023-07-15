$(document).ready(function() {
    // Function to refresh data every 5 minutes
    function refreshData() {
        $.get('/api/eplf_payments', function(data) {
            $('#eplf-payments').empty();
            data.forEach(function(id) {
                $('#eplf-payments').append('<td>' + id + '</td>');
            });
        });

        $.get('/api/eplf_logs', function(data) {
            $('#eplf-logs').empty();
            data.forEach(function(id) {
                $('#eplf-logs').append('<td>' + id + '</td>');
            });
        });

        $.get('/api/zd_payments', function(data) {
            $('#zd-payments').empty();
            data.forEach(function(id) {
                $('#zd-payments').append('<td>' + id + '</td>');
            });
        });

        $.get('/api/zd_logs', function(data) {
            $('#zd-logs').empty();
            data.forEach(function(id) {
                $('#zd-logs').append('<td>' + id + '</td>');
            });
        });
    }

    // Run refreshData immediately and then every 5 minutes
    refreshData();
    setInterval(refreshData, 300000);
});
