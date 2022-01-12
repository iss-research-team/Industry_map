
import json
import pandas as pd

def analysis(data_path, output_path):
    """
    输出某国某一类产品的贸易竞争指数（TCI）: 指一国进出口贸易的差额在进出口贸易总额中所占比重
    显性比较优势指数(ＲCA): 作为分析一国或地区某类产品比较优势具备与否的重要量化指标
    :param data_path:
    :param output_path:
    :return:
    """
    # data = csv.reader(open(data_path, 'r', encoding='unicode_escape'))
    reader = pd.read_excel(data_path)
    data = reader.values
    total_export_country = 0
    total_export_world = 0
    index_dict = {}
    for line in data:
        if line[0] != "商品分类" :
            if line[0] == "总额":
                total_export_country = line[2]
                total_export_world = line[3]
            else:
                # 使用.xlsx
                index_dict[line[0] + "TCI"] = (line[2] - line[1]) / (line[2] + line[1])
                index_dict[line[0] + "RCA"] = (line[2] / total_export_country) / (line[3] / total_export_world)
    with open(output_path, 'w', encoding='UTF-8') as file:
        json.dump(index_dict, file, ensure_ascii=False)


if __name__ == '__main__':
    data_path = "data/产品海关数据统计.xlsx"
    # data_path = "data/产品海关数据统计.csv"
    output_path = "data/产品竞争力指数.json"
    analysis(data_path, output_path)