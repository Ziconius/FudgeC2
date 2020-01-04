function export_campaign(cid){
$.ajax({
        url:`/${cid}/export_campaign`,
        type:"GET",
        success: function (response) {
            $('#FormSubmissionModal').modal({show:true})
            document.getElementById('modal-password').innerHTML = response['password'];
            document.getElementById('filename_input').value = response['filename'];
        }
    })
}


$(function() {
    $('#AddUserBtn').on('click', function (e) {
        e.preventDefault();
        var $form = $('#AnswerForm');
        $.ajax({
            url: $form.attr("action"),
            type: $form.attr("method"),
            data: $form.serialize(),
            success: function (response) {
                document.getElementById('FormModalTitle').innerHTML = response['action'];
                if (response['result'] == true) {
                    document.getElementById('modal-result').innerHTML = "<p class='text-success'>Success!</p>";
                } else {
                    document.getElementById('modal-result').innerHTML = "<p class='text-danger'>Failure!</p>";
                };
                document.getElementById('modal-reason').innerHTML = response['reason'];
                $('#FormSubmissionModal').modal({show:true})
            },
            error: function (response) {
                alert('ajax failed');
            },
        });
    });
});

// Used to filter out results in the Global settings page.
$(document).ready(function() {
    $(".search").keyup(function () {
        var searchTerm = $(".search").val();
        var listItem = $('.results tbody').children('tr');
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('")

        $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
            return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
        }
        });

        $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','false');
        });

        $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','true');
        });

        var jobCount = $('.results tbody tr[visible="true"]').length;
        $('.counter').text(jobCount + ' item');

        if(jobCount == '0') {$('.no-result').show();}
        else {$('.no-result').hide();}
    });
});