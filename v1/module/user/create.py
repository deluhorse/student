# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 2020-02-01 16:38
"""

from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('user.service', 'login', params=params)
        self.out(res)
