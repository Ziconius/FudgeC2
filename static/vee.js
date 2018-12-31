let dropdown2 = $('#dropper');
dropdown2.empty();
//dropdown.append('<option selected="true" disabled >Choose a lab to edit.</option>');
dropdown2.prop('selectedIndex', 0);
var url2 = "/api/lab/list";
// Populate dropdown with list of provinces
$.getJSON(url2, function (data) {
  $.each(data, function (key, entry) {
    dropdown2.append('<li><a href="/Labs/'+entry.id+'">'+entry.id+'. '+entry.title+'</a></li>');
  })
});

$("select").click(function() {
  var open = $(this).data("isopen");
  if(open) {
    window.location.href = "/Labs/"+$(this).val()
  }
  //set isopen to opposite so next time when use clicked select box
  //it wont trigger this event
  $(this).data("isopen", !open);
});