import hashlib
import os
import shutil
from typing import List

from fastapi import FastAPI, UploadFile
from dataset import DataSet
from api_robot import ApiRobot

app = FastAPI()


@app.post("/run/")
async def run(file: UploadFile, abstract_needed: bool = False,
              row_filters: List[str] = None, key_label: str = "标签"):
    if abstract_needed:
        col_filters = ['研究方向', '结局', 'Abstract']
    else:
        col_filters = ['研究方向', '结局']
    if row_filters == ['']:
        row_filters = ["代谢相关", "药物干预", "遗传病因"]
    else:
        row_filters = str(row_filters)[2:-2].split(',')
    filename = hashlib.md5(file.filename.encode()).hexdigest() + '.xlsx'
    with open(filename, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    dataset = DataSet(file_path=filename, col_filters=col_filters, row_filters=row_filters,
                      key_label=key_label)
    data = dataset.filtered_dict_data()
    print(data)
    output = {}
    for item in row_filters:
        print(item)
        api_robot = ApiRobot(item, data[item])
        output[item] = api_robot.query()
    if os.path.exists(filename):
        # 删除文件
        os.remove(filename)
        print(f"File {filename} deleted successfully.")
    else:
        print(f"File {filename} does not exist.")
    return output


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
