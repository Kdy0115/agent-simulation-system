var start_time = document.getElementById("start_time");
var bems_folder_place = document.getElementById("bems_folder_place");
var control_folder_place = document.getElementById("control_folder_place");
    
var layout_input_folder_place0 = document.getElementById("layout_input_folder_place0");
//var skeleton_layout_input_folder_place0 = doucment.getElementById("skeleton_layout_input_folder_place0");
var hot_position_folder_place0 = document.getElementById("hot_position_folder_place0");

var input_folder_place = document.getElementById("input_folder_place");

async function save_setting(){
    //var number_of_times = document.getElementById("number_of_times");
    //document.getElementById("output").innerHTML = number_of_times.value

    var start_time = document.getElementById("start_time");

    var bems_folder_place = document.getElementById("bems_folder_place");
    var control_folder_place = document.getElementById("control_folder_place");

    for (let j = 0; j < i; j++){
        eval("var layout_input_folder_place" + j + "= document.getElementById('layout_input_folder_place"+j+"');" );
        eval("var skeleton_layout_input_folder_place" + j + "= document.getElementById('skeleton_layout_input_folder_place"+j+"');" );
        eval("var hot_position_folder_place" + j + "= document.getElementById('hot_position_folder_place"+j+"');" );

    }
    await eel.test_print()();
    var input_folder_place = document.getElementById("input_folder_place");
    setting_check();
}




function setting_check(){
    
    document.getElementById("output").innerHTML = "現在の設定は"+"<br>"+
    
    "BEMSファイル:"+ bems_folder_place.value+"<br>"+
    "制御計画フォルダ:"+ control_folder_place.value+"<br>";
    for (let j = 0; j < i; j++){
        eval('document.getElementById("output").innerHTML += "レイアウトフォルダ'+j+':"+layout_input_folder_place'+j+'.value+"<br>"');
    }
    for (let j = 0; j < i; j++){
        eval('document.getElementById("output").innerHTML += "スケルトンフォルダ'+j+':"+skeleton_layout_input_folder_place'+j+'.value+"<br>"');
    }
    for (let j = 0; j < i; j++){
        eval('document.getElementById("output").innerHTML += "熱源情報フォルダ'+j+':"+hot_position_folder_place'+j+'.value+"<br>"');
    }

    document.getElementById("output").innerHTML +="出力先フォルダ名:"+input_folder_place.value+"<br>";

        
}

var i = 1;

setting_check();

function form_add() {
    var input_layout = document.createElement('input');
    input_layout.type = 'text';
    input_layout.id = 'layout_input_folder_place' + i;
    //input_datax.placeholder = 'x' + i;
    var parentx = document.getElementById('layout_folder_inputform');
    parentx.appendChild(input_layout);
    parentx.innerHTML += "<br>";

    var input_skeletom = document.createElement('input');
    input_skeletom.type = 'text';
    input_skeletom.id = 'skeleton_layout_input_folder_place' + i;
    //input_skeletom.placeholder = 'y' + i;
    var parenty = document.getElementById('skeletom_layout_folder_inputform');
    parenty.appendChild(input_skeletom);
    parenty.innerHTML += "<br>";

    var input_hot_positon = document.createElement('input');
    input_hot_positon.type = 'text';
    input_hot_positon.id = 'hot_position_folder_place' + i;
    //input_hot_positon.placeholder = 'y' + i;
    var parentz = document.getElementById('hot_position_folder_inputform');
    parentz.appendChild(input_hot_positon);
    parentz.innerHTML += "<br>";

    i++;
    
}

function form_remove(){
    i = i-1;
    let parentx = document.getElementById('layout_folder_inputform');
    let input_layout = document.getElementById("layout_input_folder_place"+i);
    parentx.removeChild(input_layout);
    

    let parenty = document.getElementById('skeletom_layout_folder_inputform');
    let input_skeletom = document.getElementById("skeleton_layout_input_folder_place"+i);
    parenty.removeChild(input_skeletom);

    let parentz = document.getElementById('hot_position_folder_inputform');
    let input_hot_positon = document.getElementById("hot_position_folder_place"+i);
    parentz.removeChild(input_hot_positon);
}
