# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-01 15:30
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    base_all = [
        {
            'name': '状元',
            'num': 1,
            'value': 32,
            'patten': [
                '4 4 4 4 * *',
                '1 1 1 1 1 *',
                '2 2 2 2 2 *',
                '3 3 3 3 3 *',
                '5 5 5 5 5 *',
                '6 6 6 6 6 *'
            ]
        },
        {
            'name': '榜眼',
            'num': 1,
            'value': 16,
            'patten': [
                '3 3 2 2 1 1'
            ]
        },
        {
            'name': '探花',
            'num': 1,
            'value': 16,
            'patten': [
                '6 6 5 5 4 4'
            ]
        },
        {
            'name': '会元',
            'num': 4,
            'value': 8,
            'patten': [
                '4 4 4 * * *'
            ]
        },
        {
            'name': '进士',
            'num': 8,
            'value': 4,
            'patten': [
                '1 1 1 1 * *',
                '2 2 2 2 * *',
                '3 3 3 3 * *',
                '4 4 4 4 * *',
                '5 5 5 5 * *',
                '6 6 6 6 * *'
            ]
        },
        {
            'name': '举人',
            'num': 16,
            'value': 2,
            'patten': [
                '4 4 * * * *'
            ]
        },
        {
            'name': '秀才',
            'num': 32,
            'value': 1,
            'patten': [
                '4 * * * * *'
            ]
        }
    ]

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def query_champion(self, params):
        """
        查询所欲对象
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['touzi'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        raise self._grs(self.check_patten(params))

    def check_patten(self, params):
        self.logger.info(self.date_utils.time_now())

        if isinstance(params['touzi'], str):
            params['touzi'] = self.common_utils.loads_json(params['touzi'])

        params['touzi'].sort()

        for entity in self.base_all:

            for patten in entity['patten']:
                temp_touzi = params['touzi'].copy()
                temp_patten = patten.split(" ")
                current_index = 0
                right_num = 0
                while current_index < 6:
                    if right_num == 6:
                        self.logger.info(self.date_utils.time_now())
                        return entity

                    try:
                        if temp_touzi[current_index] in temp_patten:
                            old_value = temp_touzi.pop(current_index)
                            temp_patten.remove(old_value)
                            right_num += 1
                        elif '*' in temp_patten:
                            temp_touzi.pop(current_index)
                            temp_patten.remove('*')
                            right_num += 1
                        else:
                            break

                    except Exception as e:
                        self.logger.exception(e)
