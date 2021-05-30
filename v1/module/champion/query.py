# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 2020-02-01 15:29
"""

from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('seller',), False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('champion.service', 'query_champion', params=params)
        self.out(res)
