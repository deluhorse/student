# -*- coding:utf-8 -*-

"""
@author: delu
@file: table.py
@time: 2019-11-06 23:11
"""

from base.base import Base
import tornado.gen


class Controller(Base):

    @tornado.gen.coroutine
    def post(self):

        res = {
            'code': 0,
            'msg': 'success',
            'data': {
                'row_count': 100,
                'list': [
                    {
                        'id': 1,
                        'username': 'delu1',
                        'sex': 'boy'
                    },
                    {
                        'id': 2,
                        'username': 'delu2',
                        'sex': 'girl'
                    },
                    {
                        'id': 3,
                        'username': 'delu3',
                        'sex': 'boy'
                    }
                ]
            }
        }

        print(self.json.dumps(self.request))

        self.out(res)
