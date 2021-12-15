var out_simulation_result_dir = "out/result_2021_08_23/"
var base_file_path = "data/config_data/2021_08_14_27/base/all_bems_data5.csv"
var observe_file_path = "data/config_data/observe/all/observe1.csv"
var position_data = "data/layout/position.json"
var out_file_path = 'out/result_2021_08_23//cmp/result5.csv'
var simulation_data = "out/result_2021_08_23//result5.json"
var observe_evaluation = true

async function print_evaluated_data_table(){
    console.log("表を表示します")
    //var evaluated_data = await eel.data_evaluation(out_file_path,observe_file_path,simulation_data,position_data,observe_evaluation,base_file_path)();
    var df_format = await eel.inhalation_temp_evaluation(out_file_path,base_file_path)();
    var evaluated_data = await eel.observe_temp_evaluation(observe_file_path,simulation_data,position_data)();
    console.log(df_format);
    console.log(evaluated_data);
}