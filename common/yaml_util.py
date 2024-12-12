import os
import yaml

#读取
class YamlUtil:

    def read_yaml(self,key):
        with open(os.getcwd() + '/extract.yaml', encoding='utf-8', mode='r') as f:
            value = yaml.load(f, yaml.FullLoader)
            return value[key]

    # 写入
    def write_yaml(self,data):
        with open(os.getcwd() + '/extract.yaml', encoding='utf-8', mode='a') as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    # 清空
    def clear_yaml(self):
        with open(os.getcwd() + '/extract.yaml', encoding='utf-8', mode='w') as f:
            f.truncate()


    # 读取config.yaml
    def read_config(self,one_node,two_node):
        with open(os.getcwd() + '/config.yaml', encoding='utf-8') as f:
            value = yaml.load(f, yaml.FullLoader)
            return value[one_node][two_node]

    # 读取data
    def read_data(self,yaml_name):
        with open(os.getcwd() + yaml_name, mode='r', encoding='utf-8') as f:
            value = yaml.load(f, yaml.FullLoader)
            return value
