// グローバルメニューの設定
INDEXLINK      = 'index.html';
SIMULATIONLINK = 'doing.html';
EVALUATIONLINK = 'evaluation.html';
LAYOUTLINK     = 'layout.html';

// グローバルメニューの内容
globalMenu = `
<nav class="navbar navbar-expand-lg navbar-light bg-light p-4">
  <a class="navbar-brand" href="${INDEXLINK}">BEMS温度シミュレータ 1.0 </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="${INDEXLINK}">設定 <span class="sr-only"></span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="${SIMULATIONLINK}">シミュレーション</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="${EVALUATIONLINK}">評価</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="${LAYOUTLINK}">レイアウト設定</a>
      </li>      
    </ul>
    <div class="nav-item dropdown my-2 my-lg-0">
      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
      Dropdown
      </a>
      <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
      </div>
    </div>
  </div>
</nav>
`;

document.write(globalMenu);