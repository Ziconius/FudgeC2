$(function() {
    $('#AddUserBtn').on('click', function (e) {
        e.preventDefault();
        var $form = $('#AnswerForm');
        console.log($form.serialize())
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