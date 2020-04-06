# coding: utf-8
from .usergroup import Usergroup

class NormalUserGroup(Usergroup):
    def __init__(self, name = "normalUsergroup",usernum = 1):
        super().__init__(name,usernum)
