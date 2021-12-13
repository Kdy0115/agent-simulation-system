// グローバルメニューの設定
INDEXLINK      = 'index.html';
SIMULATIONLINK = 'doing.html';
EVALUATIONLINK = 'evaluation.html';
LAYOUTLINK     = 'layout.html';

// グローバルメニューの内容
globalMenu = `
<ul id="dropdown1" class="dropdown-content">
  <li><a href="https://github.com/Kdy0115/agent-simulation-system/tree/develop_ver4" target="_blank" rel="nofollow noopener">GitHub</a></li>
  <li><a href="#">ヘルプ</a></li>
</ul>
<nav>
  <div class="nav-wrapper">
    <a href="${INDEXLINK}" class="brand-logo">BEMS温度シミュレータ</a>
    <ul class="right hide-on-med-and-down">
      <li><a href="${INDEXLINK}">設定</a></li>
      <li><a href="${SIMULATIONLINK}">シミュレーション</a></li>
      <li><a href="${EVALUATIONLINK}">評価</a></li>
      <li><a href="${LAYOUTLINK}">レイアウト設定</a></li>
      <li><a class="dropdown-trigger" href="#!" data-target="dropdown1">ドキュメント<i class="material-icons right">arrow_drop_down</i></a></li>
    </ul>
  </div>
</nav>

`;

document.write(globalMenu);

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems);
});