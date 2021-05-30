# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2019-11-21 17:06
"""
from test.tester import Tester


class MyTest(Tester):
    def update_price(self):
        # 退款成功
        self.path = 'test.service'
        self.method = 'test2'
        self.params = {
        }


if __name__ == '__main__':
    refund = MyTest()
    refund.run('update_price')