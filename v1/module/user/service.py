# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-01 16:39
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def login(self, params):
        """
        用户登陆
        :param params: 
        :return: 
        """
        if params.get('user_id'):
            raise self._grs(params)

        user_id = self.salt(6)

        raise self._grs({
            'user_id': user_id
        })
