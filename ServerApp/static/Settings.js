$(function() {
    $('#AddUserBtn').on('click', function (e) {
        e.preventDefault(); // disable the default form submit event


        var $form = $('#AnswerForm');
        console.log($form.serialize())
        $.ajax({
            url: $form.attr("action"),
            type: $form.attr("method"),
            data: $form.serialize(),
            success: function (response) {
                // if response
                //alert('response received');
                console.log("++"+response+"++")
                //if (response['result'] == true){
                    console.log(response['action'])
                    //FormModalTitle
                    //model-result
                document.getElementById('FormModalTitle').innerHTML = response['action'];
                if (response['result'] == true) {
                    document.getElementById('modal-result').innerHTML = "<p class='text-success'>Success!</p>";
                } else {
                    console.log("failing the user");
                    document.getElementById('modal-result').innerHTML = "<p class='text-danger'>Failure!</p>";
                };
                console.log("placeholder!");
                document.getElementById('modal-reason').innerHTML = response['reason'];
                //document.getElementById('FormModalTitle').innerHTML == response['action']
                $('#FormSubmissionModal').modal({show:true})
                //}
                //document.getElementById('Response').innerHTML =(response['msg']);
                // ajax success callback
                //console.log("@@@"+document.getElementById('implantCmd').innerHTML)
                //document.getElementById('implantCmd').value="";
            },
            error: function (response) {
                alert('ajax failed');
                // ajax error callback
            },

        });
        //document.getElementById('comment').innerHTML=("");//
    });
});


//