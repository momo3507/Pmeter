# coding: utf-8
import threading
import logging
import requests
import gevent
import copy
from gevent import monkey
monkey.patch_all()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
'''
定义所有线程组类的父类
'''
class Usergroup():
    def __init__(self, name="usergroup", usernum=1):
        self.name = name
        self.usernum = usernum
        self.session = requests.session()
        self.controllerlist = []
        self.httplist = []
        self.headers = {}
        self.variables = {}

    def addController(self,obj_controller):
        self.controllerlist.append(obj_controller)

    def addDefaultHeaders(self,dict_headers):
        self.headers = dict_headers

    def addHttp(self,obj_http):
        self.httplist.append(obj_http)

    def run(self):
        # for controller in self.controllerlist:
        #     controller.run()
        # for i in range(self.usernum):
        #     for http in self.httplist:
        #         http.setSession(self.session)
        #         http.run()
        #         if hasattr(http,"extract"):
        #             for key,value in http.extract.items():
        #                 self.variables[key] = value
        #                 logging.debug("%s:线程组对象当前的变量表："%threading.currentThread().name)
        #                 logging.debug("%s:%s" % (threading.currentThread().name,self.variables))
        # for i in range(self.usernum):
        #     vuser = VUser(name=self.name+"-%s"%(i+1))
        #     vuser.httplist = self.httplist.copy()
        #     vuser.start()
        #     import time
        #     time.sleep(2)
        self.vusers = []
        for i in range(self.usernum):
            self.vusers.append(gevent.spawn(self.create_vuser))
        gevent.joinall(self.vusers)
    def create_vuser(self):
        vuser = VUser()
        vuser.httplist = copy.deepcopy(self.httplist)   # 深复制对象请求对象列表，避免多协程调用参数冲突
        vuser.run()
class VUser():
    def __init__(self):
        self.session = requests.session()
        self.variables = {}
        self.httplist = []

    def run(self):
        for http in self.httplist:
            http.setSession(self.session)
            http.tgvariables = self.variables  # 设置取样器的线程变量表
            http.run()
            if hasattr(http, "extract"):
                logging.debug(http.extract.items())
                for key, value in http.extract.items():
                    self.variables[key] = value
                logging.debug("%s:%s" % (threading.currentThread().name, self.variables))




