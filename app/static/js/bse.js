/**
 *
 */

$( document ).ready(function () {

    $("#flash_msgs").delay(4000).slideUp(300);

    $('#download_all_link').click(function (e) {
        console.log('Download all link clicked');
        e.preventDefault();
        window.scrollTo(0, 0);
        $('#download_all').modal();

    });

    $("#download_all_button").click(function (e) {

        e.preventDefault();

        var url = "/download/";
        var format = $('#format3').val();
        var version = 'current';
        var archive_type = $('#archive_type').val();

        var query = url + version + '/' + format + '/' + archive_type;
        console.log(query);
        window.location = query;

        $('#download_all').modal('toggle');
    });


    $('#feedback_link').click(function (e) {
        console.log('Feedback link clicked');
        e.preventDefault();
        window.scrollTo(0, 0);

        $('#help_box_feedback').modal();

    });

    $('#about_link').click(function (e) {
        console.log('Feedback link clicked');
        e.preventDefault();
        window.scrollTo(0, 0);
        $('#help_box_about').modal();

    });

    function bind_click_event(button_id, url) {

        $(button_id).click(function(event) {

            event.preventDefault();
            $.post(url, data=$('#request_basis_Form').serialize(), function(data) {
                console.log('Data: ', data);
                if (data.status == true) {
                  $('#request_basis_dialog').modal('hide');
                  location.reload();
                }
                else {
                  $('#request_basis_dialog .modal-content').html(data);
                  bind_click_event(button_id, url);
                }
            }); //post
        }); // submit
    }

    $('#request_basis').click(function(e) {
        console.log('request basis link clicked');
        e.preventDefault();

        var url = "/request_basis/";
        $.get(url, function(data) {
            $('#request_basis_dialog .modal-content').html(data);
            $('#request_basis_dialog').modal();

            bind_click_event('#submit', url);
        }); // get
    });

});
