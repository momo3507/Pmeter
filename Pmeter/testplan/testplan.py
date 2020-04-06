# coding:utf-8
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class TestPlan:
    def __init__(self,name="Test Plan"):
        self.name = name
        self.usergrouplist = []

    def addUserGroup(self,obj_usergroup):
        self.usergrouplist.append(obj_usergroup)

    def run(self):
        logging.debug("运行测试计划: %s"%self.name)
        for usergroup in self.usergrouplist:
            usergroup.run()



