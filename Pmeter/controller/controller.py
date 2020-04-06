# coding: utf-8

class Controller():
    def __init__(self, name="controller"):
        self.name = name
        self.samplerlist = []

    def addSampler(self,obj_sampler):
        self.samplerlist.append(obj_sampler)

    def run(self):
        pass