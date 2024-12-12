import jsonpath
import requests
import json
from common.yaml_util import YamlUtil
from builtins import str
import re
from debug_talk import DebugTalk
from test import  Test


class RequestUtil:

    def __init__(self,two_node,obj):
        self.base_url=YamlUtil().read_config('base',two_node)
        self.obj=obj


    #替换值的方法
    # #(替换url，params,data,json,headers)
    # #(string，int,float,list,dict)
    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            # 判断数据类型转换成str
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            for cs in range(1, str_data.count('${') + 1):
                # 替换
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}", start_index)
                    old_value = str_data[start_index:end_index + 1]
                    print("old_value:"+old_value)
                    #反射：通过类的对象和方法字符串调用方法
                    func_name=old_value[2:old_value.index('(')]
                    args_value1=old_value[old_value.index('(')+1:old_value.index(')')]
                    new_value=""
                    if args_value1 !="" :
                        args_value2 = args_value1.split(',')
                        new_value=getattr(self.obj,func_name)(*args_value2)
                    else:
                        new_value = getattr(self.obj, func_name)()
                    if isinstance(new_value,int) or isinstance(new_value,float):
                        str_data = str_data.replace('"'+old_value+'"', str(new_value))
                    else:
                        str_data = str_data.replace(old_value, str(new_value))
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data


    #规范yaml测试用例
    def standard_yaml(self,caseinfo):
        caseinfo_keys= caseinfo.keys()
        #判断一级关键字是否包含：name，request，validate
        if "name" in caseinfo_keys and "request" in caseinfo_keys and "validate" in caseinfo_keys:
            #判断request下面是否包含：method、url
            request_keys=caseinfo["request"].keys()
            if "method" in  request_keys and "url" in request_keys:
                print("yaml基本架构检查通过")
                method = caseinfo['request'].pop("method") #pop() 函数用于移除列表中的一个元素，并且返回该元素的值。
                url= caseinfo['request'].pop("url")
                res = self.send_request(method,url,**caseinfo['request']) #caseinfo需要解包加**
                return_text=res.text
                return_code = res.status_code
                return_json=""
                try:
                    return_json = res.json()
                except Exception as e:
                    print("extract返回的结果不是JSON格式")

                # 提取值并写入extract.yaml文件
                if "extract" in caseinfo.keys():
                    for key, value in caseinfo["extract"].items():
                        if "(.*?)" in value or "(.+?)" in value:  # 正则表达式
                            zz_value = re.search(value, return_text)
                            if zz_value:
                                extract_value = {key: zz_value.group(1)}
                                YamlUtil().write_yaml(extract_value)
                        else:  # jsonpath
                            js_value = jsonpath.jsonpath(return_json, value)
                            if js_value:
                                extract_value = {key: js_value[0]}
                                YamlUtil().write_yaml(extract_value)
                #断言：
                self.assert_result(caseinfo['validate'],return_json,return_code)
            else:
                print("在request下必须包含method,url")
        else:
            print("一级关键字必须包含name,request,validate")



    sess= requests.session()

    # 统一请求封装

    def send_request(self,method,url,**kwargs):
        method=str(method).lower()  #转换小写
        #基础路径的拼接和替换
        url= self.base_url + self.replace_value(url)
        print(url)
        #参数替换
        for key,value in kwargs.items():
            if key in ['params','data','json','headers']:
                kwargs[key]=self.replace_value(value)
                print(kwargs[key])
            elif key == "files":
                for file_key, file_path in value.items():
                    value[file_key] = open(file_path, 'rb')
        res = RequestUtil.sess.request(method, url, **kwargs)
        print(res.text)
        return res
    #断言
    def assert_result(self,yq_result,sj_result,return_code):
        all_flag = 0
        for yq in yq_result:
            for key,value in yq.items():
                print(key,value)
                if key=="equals":
                    flag=self.equals_assert(value,return_code,sj_result)
                    all_flag =all_flag + flag
                elif key == 'contains':
                    flag=self.contains_assert(value,sj_result)
                    all_flag = all_flag + flag
                else:
                    print("框架暂不支持此段断言方式")
        assert all_flag==0

    # 相等断言
    def equals_assert(self,value,return_code,sj_result):
        flag=0
        for assert_key,assert_value in value.items():
            print(assert_key,assert_value)
            if assert_key=="status_code":  #状态断言
                assert_value==return_code
                if assert_value!=return_code:
                    flag=flag+1
                    print("断言失败，返回的状态码不等于%s"%assert_value)
            else:
                lists=jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
                if lists:
                    if assert_value not in lists:
                        flag=flag+1
                        print("断言失败："+assert_key+"不等于"+str(assert_value))
                else:
                    flag = flag + 1
                    print("断言失败：返回的结果不存在："+assert_key)
        return flag
    # 包含断言
    def contains_assert(self,value,sj_result):
        flag=0
        if str(value) not in str(sj_result):
            flag = flag + 1
            print("断言失败：返回的结果中不包含："+str(value))
        return flag


