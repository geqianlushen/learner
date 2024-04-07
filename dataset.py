import json

import pandas as pd


class DataSet:
    def __init__(self, file_path, col_filters, row_filters, key_label="标签"):
        self.excel_table = self.read_excel(file_path)
        self.col_filters = col_filters
        self.row_filters = row_filters
        self.key_label = key_label

    @staticmethod
    def read_excel(file_path):
        try:
            return pd.read_excel(file_path)
        except FileNotFoundError:
            print("文件未找到！")
            return
        except Exception as e:
            print("读取文件时出错:", e)
            return

    def filtered_pd_data(self, col_filters, row_filters, has_row_label=False):
        if has_row_label:
            if self.key_label in self.col_filters:
                filtered_excel_table = self.excel_table.loc[
                    self.excel_table[self.key_label].isin(row_filters), col_filters]
            else:
                filtered_excel_table = self.excel_table.loc[
                    self.excel_table[self.key_label].isin(row_filters), col_filters + [self.key_label]]
            return filtered_excel_table
        else:
            filtered_excel_table = self.excel_table.loc[self.excel_table[self.key_label].isin(row_filters), col_filters]
            return filtered_excel_table

    def filtered_json_data(self):
        filtered_pd_data = self.filtered_pd_data(self.col_filters, self.row_filters, True)
        tag_list = set(filtered_pd_data[self.key_label])
        filtered_json_data = {}
        for tag in tag_list:
            filtered_json_data[tag] = []
        for index, row in filtered_pd_data.iterrows():
            tmp_dict = {}
            for key, value in row.items():
                tmp_dict[key] = value
            tag = tmp_dict.pop(self.key_label)
            filtered_json_data[tag].append(tmp_dict)
        return json.dumps(filtered_json_data, ensure_ascii=False)

    def filtered_dict_data(self):
        filtered_pd_data = self.filtered_pd_data(self.col_filters, self.row_filters, True)
        tag_list = set(filtered_pd_data[self.key_label])
        filtered_dict_data = {}
        for tag in tag_list:
            filtered_dict_data[tag] = []
        for index, row in filtered_pd_data.iterrows():
            tmp_dict = {}
            for key, value in row.items():
                tmp_dict[key] = value
            tag = tmp_dict.pop(self.key_label)
            filtered_dict_data[tag].append(tmp_dict)
        return filtered_dict_data


# 调用函数并传入 Excel 文件路径
if __name__ == "__main__":
    Dataset = DataSet(file_path="task1.xlsx", col_filters=["IF", "Article Title"], row_filters=["代谢相关", "环境因素"],
                      key_label="标签")
    data = Dataset.filtered_json_data()
    print(data)
