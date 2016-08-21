$(document).ready(function() {
    // $('#movies_table').hide();
    $('#movies_table').DataTable( {
        "order": [[ 3, "desc"]]
    } );
    // $('#movies_table').show();
} );
