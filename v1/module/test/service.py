# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2019-11-21 17:05
"""
import tornado.gen
from tornado import httpclient
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def test(self, params):
        """
        发送通知给用户
        :param params: 
        :return: 
        """
        url = 'http://api.azoyagroup.com/v1/common/identity/verify?provider_code=identity&content=P20X0GnatI5%2F%2BNQAvtJIeY1JTnxMVB%2BXlj2IcS8E54B0NgPa41Qi2B7jr6SbP1Im%2FnSiYmuUw4y6E35lBda07y7iWOzUx8jKBn4n%2F5AM6Tg%3D&sign=e54de248b73ff061245932ef89d5960d'
        result = yield self.httputils.post(
            url,
            is_json=True
        )

        raise self._gr(result)

    @tornado.gen.coroutine
    def test1(self, params):
        """
        测试请求
        :param params:
        :return:
        """
        url = 'http://api.azoyagroup.com/v1/common/identity/verify?provider_code=identity&content=P20X0GnatI5%2F%2BNQAvtJIeY1JTnxMVB%2BXlj2IcS8E54B0NgPa41Qi2B7jr6SbP1Im%2FnSiYmuUw4y6E35lBda07y7iWOzUx8jKBn4n%2F5AM6Tg%3D&sign=e54de248b73ff061245932ef89d5960d'

        result = yield self.httputils.post(
            url,
            is_json=True
        )

        raise self._gr(result)

    @tornado.gen.coroutine
    def test2(self, params):
        """
        测试请求2
        :param params:
        :return:
        """
        client = httpclient.AsyncHTTPClient()

        url = 'http://www.gushequ.com/'

        response = yield client.fetch(
            url,
            method="POST",
            allow_nonstandard_methods=True
        )

        raise self._grs(self.common_utils.loads_json(response.body.decode('utf-8')))

    @tornado.gen.coroutine
    def test3(self, params):
        """
        测试请求3
        :param params:
        :return:
        """
        url = 'https://crossborder.mannings.com.cn/api/v1/order/status/logs/query?order_id=82019113008511005356'
        headers = {
            'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYwNDgwMCwicmVmcmVzaF9leHAiOjEyMDk2MDAsImlhdCI6MTU3NDkxMzcxMCwidXNlcl90eXBlIjoic2VsbGVyIiwiZ3JvdXBfaWQiOjAsInNob3BfaWQiOiI3Iiwic2hvcF9uYW1lIjoiXHU4NDJjXHU1YmU3IiwiYWRtaW5faWQiOjIxfQ.bSwO9vujT8mEkPTgBImPta4Ccg_UECRI1YroiZYOB48'
        }
        success = 0
        for i in range(100):
            try:
                result = yield self.httputils.get(
                    url,
                    headers=headers,
                    is_json=True
                )
                self.logger.info(result)
                success += 1
            except Exception as e:
                self.logger.exception(e)
        self.logger.info(success)

        raise self._grs()
