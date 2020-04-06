# coding: utf-8
"""
通过jsonpath提取
"""
from jsonpath import jsonpath
from .extractor import Extractor

class JsonExtractor(Extractor):
    def __init__(self, extractjson,extpath):
        super().__init__(extractjson)
        self.extpath = extpath
        self.res = jsonpath(self.extractjson,self.extpath)
        if self.res:
            self.res = self.res[0]


if __name__ == '__main__':
    a = {"name":"wangwei"}
    b = "$.name"

    c = JsonExtractor(a,b).res
    print(c)