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

    var $target = document.querySelector('.config-stop-button');
    $target.classList.toggle('is-hidden')
});


function renderToConsole(config){
  render = `
    <ul>
      <li>シミュレーション回数：${config[0]}回（分）</li>
      <li>出力先フォルダ名：${config[1]}</li>
      <li>BEMSファイル名：${config[2]}</li>
      <li>制御計画フォルダ名：${config[3]}</li>
      <li>熱源情報ファイル名：${config[4]}</li>
      <li>レイアウト情報ファイル名：${config[5]}</li>
      <li>マルチプロセス：${config[6]}</li>
    </ul>
  `;
  var target = document.getElementById("simulation-console");
  target.innerHTML = render;
}

async function start_simulation(){
  res = await eel.config_import()();
  renderToConsole(res);
  await eel.prepare_simulation()();
  // await eel.create_simulation_process()();
  $(".message-start").show();
  $(function(){
    $(".message-start:not(:animated)").fadeIn("slow",function(){
      $(this).delay(1000).fadeOut("slow");
    });
  });
  var $target = document.querySelector('.config-start-button');
  $target.classList.toggle('is-hidden');
  var $target_ = document.querySelector('.config-stop-button');
  $target_.classList.toggle('is-hidden');
}

async function stop_simulation(){
  await eel.exit_simulation()();
  $(".message-stop").show();
  $(function(){
    $(".message-stop:not(:animated)").fadeIn("slow",function(){
      $(this).delay(1000).fadeOut("slow");
    });
  });

  var $target = document.querySelector('.config-start-button');
  $target.classList.toggle('is-hidden');
  var $target_ = document.querySelector('.config-stop-button');
  $target_.classList.toggle('is-hidden');

  var target = document.getElementById("simulation-console");
  target.innerHTML = "";
}