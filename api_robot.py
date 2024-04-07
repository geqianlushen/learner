import json

import requests

from dataset import DataSet


class ApiRobot:
    def __init__(self, tag, dataset, config_file="robot_config.json"):
        self.tag = tag
        self.dataset = dataset
        self.doc_num = len(self.dataset)
        self.config = self.load_config(config_file)
        self.prompt = self.get_prompt()
        self.api = self.get_api()
        self.format = f'''
                            {self.doc_num}篇文章总体研究主要方向为***。
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                xx（xx为类似结论的篇数）篇文献对（***进行了总结或提供了***方向或研究表明了***）;
                                ...（按照上述句式续写）
                            '''

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_prompt(self):
        for tags in self.config['Prompts']:
            for tag in self.config['Prompts'][tags]:
                return self.config['Prompts'][tags][tag]

    def get_api(self):
        if self.tag in self.config['Api_repo']:
            return self.config['Api_repo'][self.tag]

    def gen_payload(self):
        return {"question": f'{self.dataset}',
                "overrideConfig": {
                    "systemMessagePrompt": "作为一名{tag}专家，根据用户给的{doc_num}篇文献内容作为知识库，请根据归纳策略给出归纳结果。归纳策略：标签为药物干预的回复格式严格按照：{format}而其他标签的回复格式案例:“xx（xx为具体数字）篇文献对***进行***，为***提供（总结/发现/结论等等）**”格式回答，自由组合，将所有的文献都体现在总结里。例如：研究主要方向为***，其中：xx篇文献对***进行了总结，xx篇文献对***提供了方向，xx篇文章研究表明***等。请注意，所有文章都需在总结中体现,由研究方向+结局构成，但研究方向相似的请归纳在一起，文献总数不能出错，回答简洁，无需每篇都总结，请用专业术语，不要打招呼说多余的客套话。请重点关注这些知识点：{prompt}",
                    "humanMessagePrompt": "知识库总共有{doc_num}篇文献，内容如下：{question}",
                    "promptValues": {
                        "tag": self.tag,
                        "doc_num": self.doc_num,
                        "format": self.format,
                        "prompt": self.prompt,
                        "dataset": self.dataset
                    }
                }}

    def query(self, outputfile=""):
        try:
            response = requests.post(self.api, json=self.gen_payload())
            response.raise_for_status()
            response = response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求异常:{e}")
            response = None
        if response is not None:
            # output_content = f'有关{self.tag}的{self.doc_num}篇文献\n' + str(response['text'])
            output_content = str(response['text']).replace("\n", "")
            if outputfile:
                # 打开文件以追加模式写入数据
                with open(outputfile, 'a') as file:
                    file.write("\n")  # 添加换行以确保新内容独立一行
                    file.write(output_content)
            else:
                return output_content
        else:
            print("无法连接到API，请检查你的网络连接.")


if __name__ == '__main__':
    Dataset = DataSet(file_path="task1.xlsx", col_filters=['研究方向', '结局', '标签'],
                      row_filters=["遗传病因", "环境因素"],
                      key_label="标签")
    data = Dataset.filtered_dict_data()
    api_robot = ApiRobot("遗传病因", data["遗传病因", "环境因素"])
    output = api_robot.query()
    print(output)
