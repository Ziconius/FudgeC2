function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Reorders the response data of Get_ImplantCallback
function order_response_by_time ( response ){
    var a = 0;
    var ordered_list = [];
    var change = true;
    for ( element in response){
        ordered_list.push(response[element])
    }
    while ( change ){
        change = false;
        len = ordered_list.length;
        for (element in ordered_list){
            y = Number(element)+1;
            x = Number(element);
            if (y >= len){
            } else if (ordered_list[x].last_checked_in < ordered_list[y].last_checked_in) {
                var b = ordered_list[y];
                ordered_list[y] = ordered_list[x];
                ordered_list[x] = b;
                change = true;
                break;
            }
        }
    }
    return ordered_list
}

// Outputs the status of registered implants.
async function Get_ImplantCallback (cid){
    while(true){
        $.ajax({
            url:`/${cid}/implant/status`,
            type:"GET",
            success: function (response) {

                var implant_status_text = ""
                response = order_response_by_time ( response )
                for (element in response){
                    var pageContainer = document.getElementById('ImplantStatusValues')
                    var utcSeconds = response[element].last_checked_in;
                    var d = new Date(0);
                    d.setUTCSeconds(utcSeconds);
                    var date = new Date(response[element].last_checked_in*1000);
                    var year = date.getFullYear();
                    var month = date.getMonth();
                    var day = date.getDate();
                    var hours = date.getHours();
                    var minutes = "0" + date.getMinutes();
                    var seconds = "0" + date.getSeconds();
                    time_last_seen = hours+":"+minutes.substr(-2)+':'+seconds.substr(-2)+' '+day+'/'+month+'/'+year

                    var CodeColour = "text-primary"
                    if (response[element].status=='poor'){
                        var CodeColour="text-danger"
                    } else if (response[element].status=='normal') {
                        var CodeColour="text-warning"
                    } else if (response[element].status=='good') {
                        var CodeColour="text-success"
                    }
                    Entry = "<div class=''><p>Title: "+response[element].title+"<br>Time: "+time_last_seen+"<br>Status: <code class='"+CodeColour+"'>"+response[element].status+"</code></p></div><hr>"
                    implant_status_text += Entry;
                }
            document.getElementById('ImplantStatusValues').innerHTML = "" // Clear current implants before writing updated values.
            document.getElementById('ImplantStatusValues').innerHTML = implant_status_text
            }
        })
    // Import the handling of this loop
    await sleep(15000);
    }
};

// Output the commands which are registered and awaiting pickup by the implant.
async function Get_Awaiting_Cmds (cid){
    while(true){
        $.ajax({
            url:`/${cid}/waiting_commands`,
            type:"GET",
            success: function (response) {
                document.getElementById('awaiting').innerHTML = ""
                for (element in response){
                    if (response[element].read_by_implant == 0){
                        line="<p>Implant ID: "+response[element].uik+"</br>Command: "+response[element].log_entry+"</p>"
                        document.getElementById('awaiting').innerHTML =  document.getElementById('awaiting').innerHTML + line
                    } else {
                        //console.log(response[element].time)
                    }
                }
            }
        })
    await sleep(15000);
    }
};