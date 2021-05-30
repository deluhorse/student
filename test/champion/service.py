# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-01 16:10
"""
from test.tester import Tester


class MyTest(Tester):
    def query_champion(self):
        # 退款成功
        self.path = 'champion.service'
        self.method = 'query_champion'
        self.params = {
            'touzi': ["6", "2", "6", "6", "6", "6"]
        }


if __name__ == '__main__':
    refund = MyTest()
    refund.run('query_champion')
