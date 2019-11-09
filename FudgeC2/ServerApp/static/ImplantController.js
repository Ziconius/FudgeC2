function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function unix_to_human_time(unixtime){
    var utcSeconds = unixtime;
    var d = new Date(0);
    d.setUTCSeconds(utcSeconds);
    var date = new Date(unixtime*1000);
    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDate();
    var hours = "0" + date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    time_last_seen = hours.substr(-2)+":"+minutes.substr(-2)+':'+seconds.substr(-2)+' '+day+'/'+month+'/'+year
    return time_last_seen
}
// OnClick for implant command submission found on http[s]://<ip>/<campaign-id>/
$(function() {
    $('#AnswerBtn').on('click', function (e) {
        e.preventDefault(); // disable the default form submit event
        var $form = $('#AnswerForm');
        $.ajax({
            url: $form.attr("action"),
            type: $form.attr("method"),
            data: $form.serialize(),
            success: function (response) {
                document.getElementById('implantCmd').value="";
                if (response['cmd_reg']['result']===false){alert(response['cmd_reg']['reason'])}
            },
            error: function (response) {
                alert('ajax failed');
            },

        });
    });
});

// This order active implants by their most recent check in time.
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



async function get_active_implant_command_queue (cid){
    $.ajax({
        url:`/api/v1/campaign/${cid}/implants/queued`,
        type:"GET",
        success: function (response) {
            document.getElementById('awaiting').innerHTML = ""
            for (element in response){
                if (response[element].read_by_implant == 0){
                    line="<p>Implant ID: "+response[element].uik+"</br>Command: "+response[element].log_entry+"</p>"
                    document.getElementById('awaiting').innerHTML =  document.getElementById('awaiting').innerHTML + line
                } else {
                    // console.log("Error:"+response[element].time)
                }
            }
        }
    })
}


async function get_active_implant_state (cid){
$.ajax({
            url: `/api/v1/campaign/${cid}/implants/state`,
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
                    // Generate link to implant details page:
                    title_and_link = 'Title: <a href="/' + cid + '/implant/active/' + response[element].implant_id + '">' + response[element].title + '</a>'
                    Entry = "<div class=''>" + title_and_link + "<br>Time: " + time_last_seen+"<br>Status: <code class='"+CodeColour+"'>"+response[element].status+"</code></p></div><hr>"
                    implant_status_text += Entry;
                }
            document.getElementById('ImplantStatusValues').innerHTML = "" // Clear current implants before writing updated values.
            document.getElementById('ImplantStatusValues').innerHTML = implant_status_text
            }
        })
}

var contained_list=[];
var c_state=0
function get_command_responses(cid){
    $.ajax({
        url:`/api/v1/campaign/${cid}/implants/response`,
        type:"GET",
        success: function (response) {
            // Get list of responses
            var pageContainer = document.getElementById('Response');
            for (element in response){
                // Check for the log_id existing, if it doesn't add to list and write to top of page to remove weird loading page
                if ( contained_list.includes(response[element].log_id) ) {
                    //console.log('Entry found');
                } else {

                    contained_list.push(response[element].log_id);
                    // pageContainer = response[element].log_id+ pageContainer;
                    // alert(pageContainer)
                    GG = response[element].log_id;
                    var utcSeconds = response[element].time;
                    var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
                    d=unix_to_human_time(response[element].time)
                    // console.log(response[element]);
                    tmp_text = response[element].log_entry
                    response_data = tmp_text.replace(new RegExp('\r?\n','g'), '<br />');
                    if (c_state === 0){
                        bgc = '<div class="p-1 bg-light">'
                        c_state = 1
                     } else {
                        bgc = '<div class="p-2">'
                        c_state  = 0
                    }

                    GG = bgc+"<p>Name: "+response[element].title+"<br>Time: "+d+"<br>Response:<br> <code>"+response_data+"</code></p></div>";
                    WP = document.getElementById('Response').innerHTML;
                    // alert(WP);
                    document.getElementById('Response').innerHTML = GG + WP;
                 }
               }
            //console.log(contained_list)
            }
    })
}


async function implant_page_controller (cid){
    delay = 0
    while (true)
    {
        // Run each of the checks for new command responses, active implants, and queued commands with a delay between each of $delay
        get_active_implant_state(cid)
        await sleep(delay)

        get_active_implant_command_queue(cid)
        await sleep(delay)

        get_command_responses(cid)
        await sleep(delay)
        delay = 2000
    }
}

function get_overview_page_details(){

    $.ajax({
        url:`/api/v1/campaign`,
        type:"GET",
        success: function (response) {

            for (element in response){
                console.log("aaaaa")
                get_campaign_info_by_id(response, element)

            }
            document.getElementById('campaign-info').innerHTML = t_top
        }
    })
    get_listener_info()
}

function get_listener_info(){
    $.ajax({
        url:`/api/v1/listener`,
        type:"GET",
        success: function (response) {
            for (x in response){
                console.log(response)
                A=response[x]['common_name']
                B = response[x]['port']
                C= response[x]['type']
                D =response[x]['state']

                E = document.getElementById('t_body_listener').innerHTML;
                line = `<td>${A}</td><td>${B}</td><td>${C}</td><td>${D}</td>`
                document.getElementById('t_body_listener').innerHTML = E + line;
            }
        }
    })
}


function get_campaign_info_by_id(rrr, cid){
    $.ajax({
        url:`/api/v1/campaign/${cid}/implants/active`,
        type:"GET",
        success: function (response) {
            for (item in response){
//                console.log(response[item])
                A = rrr[cid]
                A = `<a href="/${cid}">${A}</a>`
                B = response[item]['generated_title']
                b = response[item]['unique_implant_id']
                B =`<a href="/${cid}/implant/active/${b}">${B}</a>`
                C = response[item]['last_check_in']
                D = response[item]['callback_url']

    //            for (element in response){
    //                console.log(response[element])
    //            }
                E = document.getElementById('t_body').innerHTML;

                line = `<td>${A}</td><td>${B}</td><td>${C}</td><td>${D}</td>`
                document.getElementById('t_body').innerHTML = E + line;
//                console.log("ret: "+response)

            }


            return response;
        }
    })
}





function print(data){
    console.log(camp_implants)
    for (x in camp_implants){
        console.log("aaa: "+camp_implants[x])
        campaign_name = camp_implants[x]['generated_title']
        implant_name = "b"
        checkin_time = "c"
        a = `<tr><td>${campaign_name}</td><td>${implant_name}</td><td>${checkin_time}</td></tr>`
        t_top = t_top + a
    }


}
