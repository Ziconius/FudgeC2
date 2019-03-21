function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function Get_ImplantCallback (cid){
    while(true){
        $.ajax({
            url:`/${cid}/implant/status`,
            type:"GET",
            success: function (response) {
                document.getElementById('ImplantStatusValues').innerHTML = ""
                for (element in response){
                    //contained_list.push(response[element].title)
                    var pageContainer = document.getElementById('ImplantStatusValues')
                    //var GG = response[element].title;
                    var utcSeconds = response[element].last_checked_in;
                    var d = new Date(0);
                    d.setUTCSeconds(utcSeconds);
                    var CodeColour = "text-primary"
                    if (response[element].status=='poor'){
                        var CodeColour="text-danger"
                    } else if (response[element].status=='normal') {
                        var CodeColour="text-warning"
                    } else if (response[element].status=='good') {
                        var CodeColour="text-success"
                    }
                    GG = "<div class=''><p>Title: "+response[element].title+"<br>Time: "+d+"<br>Status: <code class='"+CodeColour+"'>"+response[element].status+"</code></p></div><hr>"
                    document.getElementById('ImplantStatusValues').innerHTML = document.getElementById('ImplantStatusValues').innerHTML + GG;
                }
            }
        })
    await sleep(15000);
    }
};


async function Get_Awaiting_Cmds (cid){
    while(true){
        $.ajax({
            url:`/${cid}/waiting_commands`,
            type:"GET",
            success: function (response) {
                document.getElementById('awaiting').innerHTML = ""
                //    document.getElementById('awaiting').innerHTML = response
                for (element in response){
                    //contained_list.push(response[element].title)
                    //var pageContainer = document.getElementById('awaiting')
                    if (response[element].read_by_implant == 0){
                        console.log(response[element].time)
                        line="<p>Implant ID: "+response[element].uik+"</br>Command: "+response[element].log_entry+"</p>"
                        document.getElementById('awaiting').innerHTML =  document.getElementById('awaiting').innerHTML + line
                    } else { console.log(response[element].time)}
                }
            }
        })
    await sleep(15000);
    }
};