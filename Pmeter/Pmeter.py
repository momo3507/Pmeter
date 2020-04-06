# coding: utf-8
import logging
import yaml
from .parse import *
from .testplan.testplan import TestPlan
from .usergroup.usergroup import Usergroup
from .sampler.httpsampler import HttpSampler
from .extractor.extractor import Extractor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Pmeter:
    def __init__(self, file_pmeter):
        self.file_pmeter = file_pmeter
        with open(self.file_pmeter,"r",encoding="utf-8") as f:
            self.file_obj = f.read()
        self.file_json = yaml.load(self.file_obj,Loader=yaml.FullLoader)    # 测试文件转结构体
        self.testplan = self.file_json.get("TestPlan")  # 获取测试计划结构体
        self.variables = self.testplan.get("ele-Variables") # 获取测试计划的变量表
        self.HttpRequestDefaults = self.file_json.get("ele-HttpRequestDefaults")    #获取请求默认值
        self.testplan_name = self.testplan.get("proty-name")    # 获取测试计划名称
        self.obj_testplan = TestPlan(name=self.testplan_name)   # 创建测试计划对象
        self.__intoBox()    # 元素装箱，组装测试计划对象

    def run(self):
        logging.info("开始执行测试: --{test_plan_name}--".format(test_plan_name=self.testplan_name))
        self.obj_testplan.run()


    def __intoBox(self):
        # element into box
        self.threadsgroups = self.__getThreadGroups()
        for threadgroup in self.threadsgroups:
            # create threadgroup obj
            self.obj_threadgroup = Usergroup(name=threadgroup.get("proty-name"), usernum=threadgroup.get("proty-num"))
            # threadgroup obj into testplan obj
            self.obj_testplan.addUserGroup(self.obj_threadgroup)
            # get the httplist of the treadgroup
            self.httplist = self.__getHttpList(threadgroup)
            if self.httplist:
                for http in self.httplist:
                    # create http obj
                    self.obj_http = self.__creatHttpObj(http)
                    # http obj into threadgroup obj
                    self.obj_threadgroup.addHttp(self.obj_http)


    def __getThreadGroups(self):
        # 获取线程组列表
        self.__grouplist = self.testplan.get("ele-ThreadGroups")
        if self.__grouplist:
            return self.__grouplist
        else:
            raise Exception("Need at least one ele-ThreadGroup")


    def __getHttpList(self,elethreadgroup):
        # 获取请求列表
        self.__httplist = elethreadgroup.get("ele-HttpSteps")
        if self.__httplist:
            return self.__httplist
        else:
            return None


    def __creatHttpObj(self,http):
        # 根据http结构体创建http对象
        self.__http_name = http.get("proty-name")
        self.__http_protocol = http.get("proty-Protocol") if http.get(
            "proty-Protocol") else self.testplan.get("ele-HttpRequestDefaults").get(
            "proty-Protocol")
        self.__http_ip = http.get("proty-ServerNameOrIp") if http.get(
            "proty-ServerNameOrIp") else self.testplan.get("ele-HttpRequestDefaults").get(
            "proty-ServerNameOrIp")
        self.__http_port = http.get("proty-Port") if http.get(
            "proty-Port") else self.testplan.get("ele-HttpRequestDefaults").get(
            "proty-Port")
        self.__http_headers = http.get("proty-Headers") if http.get(
            "proty-Headers") else self.testplan.get("ele-HttpHeaderDefaults")

        self.__http_method = http.get("proty-Method")
        self.__http_path = http.get("proty-Path")
        self.__http_params = http.get("proty-Params")
        self.__http_body = http.get("proty-Body")
        if isinstance(self.__http_body, dict):  # 如果参数是json
            self.__http_data = None
            self.__http_json = self.__http_body
        else:
            self.__http_data = self.__http_body
            self.__http_json = None
        self.__http = HttpSampler(name=self.__http_name, method=self.__http_method,
                                url="{protocol}://{ip}:{port}{path}".format(
                                    protocol=self.__http_protocol, ip=self.__http_ip, port=self.__http_port,
                                    path=self.__http_path), params=self.__http_params, data=self.__http_data,
                                json=self.__http_json,headers=self.__http_headers)
        self.__http_extract = http.get("ele-extract")
        if self.__http_extract:
            self.__http.addExtract(Extractor(self.__http_extract))

        self.__http.tpvariables = self.variables # 设置取样器的测试计划变量表
        # self.__http.parselist = [Parse(self.__http_params, self.variables),
        #                      Parse(self.__http_json, self.variables)]  # 设置http对象的parselist属性
        # 将变量和函数转为值
        return self.__http





