# coding: utf-8
from .sampler import Sampler
from ..extractor.jsonextractor import JsonExtractor
from ..parse import *
import logging
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class HttpSampler(Sampler):
    def __init__(self, name="http sampler", method="GET", url="", params=None, data=None, json=None, **kwargs):
        super().__init__(name)
        self.method = method.upper()
        self.url = url
        self.params = params  # 用于GET请求
        self.data = data  # 用于POST请求
        self.json = json  # 用于POST请求
        self.kwargs = kwargs
        logging.debug(self.params)
        logging.debug(self.json)
        logging.debug(self.kwargs)
        self.parselist = []
        self.tpvariables = {}
        self.tgvariables = {}

    def addExtract(self, obj_extract):  # 提取器
        self.extractor = obj_extract.extractjson
        self.extract = {}

    def setSession(self, obj_session):
        self.session = obj_session

    def run(self):
        logging.debug("运行取样器: %s" % self.name)
        logging.debug("%s请求参数是:%s"%(threading.currentThread().name,self.params))
        self.parselist = [Parse(property, self.tgvariables, self.tpvariables) for property in [self.params,self.json]]  # 设置http对象的parselist属性
        self.parsekwargs = [Parse(self.kwargs[key], self.tgvariables, self.tpvariables)for key in self.kwargs.keys()]
        for parse in self.parselist:
            parse.run()
        for parse in self.parsekwargs:
            parse.run()
        logging.debug("Send Http('method':{method},'url':{url},'params':{params},'data':{data},'json':{json})".format(
            method=self.method, url=self.url, params=self.params, data=self.data, json=self.json))

        if self.method == "GET":
            self.res = self.session.get(url=self.url, params=self.params, **self.kwargs)
        elif self.method == "POST":
            self.res = self.session.post(self.url, params=self.params, data=self.data, json=self.json,
                                         **self.kwargs)
        logging.debug(self.res.status_code)
        logging.debug(self.res.content)
        if hasattr(self, "extractor"):
            logging.debug("检测到有提取器")
            for varname, path in self.extractor.items():
                logging.debug(self.res.json())
                logging.debug(path)
                self.extract[varname] = JsonExtractor(self.res.json(), path).res
            logging.debug(self.extract)
