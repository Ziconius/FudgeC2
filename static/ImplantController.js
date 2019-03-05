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
                    GG = "<div class=''><p>title: "+response[element].title+"<br>Time: "+d+"<br>status: <code>"+response[element].status+"</code></p></div><hr>"
                    document.getElementById('ImplantStatusValues').innerHTML = document.getElementById('ImplantStatusValues').innerHTML + GG;
                }
            }
        })
    await sleep(15000);
    }
};