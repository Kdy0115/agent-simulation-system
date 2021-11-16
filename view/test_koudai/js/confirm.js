async function import_dirs(){
    return await eel.render_dir()();
}

async function import_floors(val){
    return await eel.render_floors(val)();
}

function render_graphes(result){

}
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems);

    import_dirs().then(function (gli) {
        var target = document.getElementById("input-select");
        for(i=0; i<gli.length; i++){
            var option = document.createElement("option");
            option.text = gli[i];
            option.value = gli[i];
            target.appendChild(option);
        }
    });
});

$('#input-select').change(function() {
    console.log($(this).val());
    var target = document.getElementById("floor-select");
    if ($(this).val() == "nothing"){
        target.disabled = true;
        target.innerHTML = "";
        var option = document.createElement("option");
        option.text = "結果フォルダを選択してください";
        option.value = "nothing";
        target.appendChild(option);
    } else {
        target.disabled = false;
        import_floors($(this).val()).then(function (val) {
            var target = document.getElementById("floor-select");
            target.innerHTML = "";
            for(i=0; i<val.length; i++){
                var option = document.createElement("option");
                option.text = val[i];
                option.value = val[i];
                target.appendChild(option);
            }
        })
    }
  });

async function import_result_data(path){
    return await eel.import_result_data(path)();
}
function post_result(){
    if ($('#input-select').val() == "nothing"){
        alert("結果フォルダを選択してください")
    } else{
        $('.all-loading-screen').show();
        var dir = $('#input-select').val();
        var file = $('#floor-select').val();
        var path = 'out/' + dir + '/' + file;
        import_result_data(path).then(function (result) {
            render_heatmap(result).then(function (value){
                $('.all-loading-screen').hide();
            });
        });
    }
}