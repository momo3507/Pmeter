# coding: utf-8
"""
定义所有提取器的父类
"""
class Extractor:
    def __init__(self,extractjson):
        '''

        :param extractjson: this is a json like {"token":"$.content.token"}
        '''
        self.extractjson = extractjson

    def run(self):
        pass