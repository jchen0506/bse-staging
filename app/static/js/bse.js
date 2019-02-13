/**
 *
 */

$( document ).ready(function () {

    $('#download_all_link').click(function (e) {
        console.log('Download all link clicked');
        e.preventDefault();
        window.scrollTo(0, 0);
        $('#download_all').modal();

    });

    $("#download_all_button").click(function (e) {

        e.preventDefault();

        var url = "/download/";
        var format = $('#format2').val();
        var version = 'current';
        var archive_type = $('#archive_type').val()

        var query = url + version + '/' + format + '/' + archive_type;
        console.log(query)
        window.location = query

        $('#download_all').modal('toggle');
    });

});
