async function render_config() {
  var res = await eel.config_import()();
  var inputs = document.getElementsByTagName("input");
  for(var i=0; i<res.length - 1; i++){
    inputs[i].value = res[i];
  }
  var element = document.getElementsByTagName( "option" ) ;
  if (res[i] == "True"){
    element[0].selected = true;
  } else{
    element[1].selected = true;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var options = {
    "container":"li"
  }
  var elems_select = document.querySelectorAll('select');
  var instances_select = M.FormSelect.init(elems_select);
  var elems_modal = document.querySelectorAll('.modal');
  var instances_modal = M.Modal.init(elems_modal);
  var instances = M.Dropdown.init(elems);
  render_config();
});


async function saveConfigure(){
  var inputs = document.getElementsByTagName("input");
  await eel.configure_save(inputs[0].value, inputs[1].value, inputs[2].value, inputs[3].value, inputs[4].value, inputs[5].value, inputs[6].value)();
  $("#message").show();
  $(function(){
    $(".message:not(:animated)").fadeIn("slow",function(){
      $(this).delay(1000).fadeOut("slow");
    });
  });
}

