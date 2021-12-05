/*
data = [0]
first()

async function first(){
    var res = await eel.config_import()();
    output_folder_path = res[7];
    data = await eel.import_result_data(output_folder_path)();
    console.log(data[3]);
}
*/

async function start_simulation(){
    
    await eel.start_simulation()();
}
async function stop_simulation(){
    await eel.stop_simulation()();
}

async function print_heatmap(){
    var res = await eel.config_import()();
    output_folder_path = res[7];
    console.log(output_folder_path);
    data = await eel.import_result_data(output_folder_path)();
    console.log(data[0]);
    heatmap_data = [data[0],data[1]];
    await eel.print_heatmap(heatmap_data)();

}


/*
var mydata = {
    labels: ["１月", "２月", "３月", "４月", "５月", "６月", "７月"],
    datasets: [
      {
        label: '数量',
        hoverBackgroundColor: "rgba(0,0,0,1)",
        data: [880, 740, 900, 520, 930],
        lineTension: 0,
        fill: false,
      }
    ]
  };
  
  //「オプション設定」
  var options = {
    scales: {
        yAxes: [{
            ticks: {
                
                beginAtZero: true
            }
        }]
    }
};
  
  var canvas = document.getElementById('stage');
  var chart = new Chart(canvas, {
  
    type: 'line',  //グラフの種類
    data: mydata,  //表示するデータ
    options: options  //オプション設定
  
  });

const mapHeight = 20;
const mapWidth = 40;

const maxVal = 741;  // 追加

// データセットの生成
const generateDatasets = function(){
  const datasets = []
  for(let i=0; i<mapHeight; i++){
    datasets.push({
      data: new Array(mapWidth).fill(1),
      borderWidth: 0.2,
      borderColor: "#FFFFFF",
      backgroundColor: generateColor(i)   // 変更
    })
  }
  return datasets    
}

// 色配列の生成 (追加）
const generateColor = function(y){
  const datasetColors = []
  for(let x=0; x<mapWidth; x++){
    const opa = ((x * y / maxVal)*0.7 + 0.3).toFixed(2);
    datasetColors.push("rgba(135,206,235," + opa + ")")
  }
  return datasetColors
}

// データラベルの生成
const generateLabels = function(){
  let labels = []
  for (var i=1; i<mapWidth+1; i++){
    labels.push(i)
  }
  return labels
}

const ctx = document.getElementById('heatMap').getContext('2d')
const heatMap = new Chart(ctx, {
  type: 'bar',
  data: {
    datasets: generateDatasets(),
    labels: generateLabels()
  },
  options: {
    title: {
      display: true,
      text: 'Heat Map Sample',
      fontSize: 18,
    },
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          color: '#FFFFFF',
        },
        barPercentage: 0.99,
        categoryPercentage: 0.99,
        stacked: true,
        ticks: {
          min: 0,
          display: false,
        }
      }],
      yAxes: [{
        gridLines: {
          color: '#FFFFFF',
          zeroLineWidth: 0
        },
        stacked: true,
        ticks: {
          min: 0,
          stepSize: 1,
          display: false
        }
      }]
    },
  }
});
*/

