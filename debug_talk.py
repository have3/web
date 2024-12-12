import random
import time
from common.yaml_util import YamlUtil

class DebugTalk:

    #获得随机数
    def get_random_number(self,min,max):
        rm=random.randint(int(min),int(max))
        return str(rm)

    #读取extract.yaml文件中的值
    def read_extract_data(self,key):
        return YamlUtil().read_yaml(key)
