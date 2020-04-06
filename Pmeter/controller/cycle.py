# coding: utf-8
'''
定义控制器的子类：循环控制器
'''
from .controller import Controller
class Cycle(Controller):
    def __init__(self, name="cycle controller",times=1):
        super().__init__(name)
        self.times = times

    def run(self):
        if self.times > 0:
            for i in range(self.times):
                for sampler in self.samplerlist:
                    sampler.run()
