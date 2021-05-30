# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""
import json
import cgi
import time
import hashlib
import random
from html.parser import HTMLParser
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger

pay_type_dict = {
    '1': 'alipay',
    '3': 'wechat',
    '4': 'bonus',
    '5': 'epayments',
    '6': 'paypal',
    '8': 'drp_balance'
}


class CommonUtil(object):
    @staticmethod
    def return_val(data, default_val=None):
        """
        有值返回，无值返回空字符串
        :param data:
        :param default_val:
        :return:
        """
        if data or data == 0:
            return data
        else:
            return '' if default_val is None else default_val

    @staticmethod
    def get_val(dict_params, key, default=''):
        """
        从字典中获取数据
        1 如果key不存在并且dict_params[key]不是None，返回dict_params[key]
        2 否则返回空字符串
        :param dict_params: 字典
        :param key: key
        :param default: default
        :return:
        """
        if key in dict_params and dict_params[key]:
            return dict_params[key]
        else:
            return default if default != '' else ''

    @staticmethod
    def remove_element(my_dict, element_list):
        """
        移除字典中的元素
        :param my_dict: 
        :param element_list: 
        :return: 
        """
        for element in element_list:

            if element in my_dict:
                my_dict.pop(element)
        return my_dict

    @staticmethod
    def is_empty(key_list, my_dict):
        """
        判断key_list中的元素是否存在为空的情况
        :param key_list: 
        :param my_dict: 
        :return: 
        """
        for key in key_list:
            if key not in my_dict or not my_dict[key]:
                return True
        return False

    @staticmethod
    def is_inexist(key_list, my_dict):
        """
        判断key_list中的元素是否不存在
        :param key_list:
        :param my_dict:
        :return:
        """
        for key in key_list:
            if key not in my_dict:
                return True
        return False

    @staticmethod
    def get_images(images):
        """
        将图片json转换成图片地址
        :param images: 
        :return: 
        """
        if isinstance(images, dict):
            return properties.get('images', 'HOST_TYPE_' + str(images['type'])) + images['key']

        try:
            result = []
            image_data = json.loads(images)
        except Exception as e:
            # 如果字符串为空，返回空列表，否则返回url
            new_image_list = []
            if images and len(images) > 0:
                new_image_list.append(images)
            return new_image_list

        if isinstance(image_data, dict):
            return properties.get('images', 'HOST_TYPE_' + str(image_data['type'])) + image_data['key']
        elif isinstance(image_data, list):
            try:
                for image in image_data:
                    result.append(properties.get('images', 'HOST_TYPE_' + str(image['type'])) + image['key'])
                return result
            except Exception as e:
                return image_data
        return image_data

    @staticmethod
    def escape_html(content):
        """
        将HTML转义
        :param content:
        :return:
        """
        return cgi.escape(content)

    @staticmethod
    def un_escape_html(content):
        """
        反转HTML
        :param content:
        :return:
        """
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(content)

    @classmethod
    def salt(cls, salt_len=6, is_num=False, chrset=''):
        """
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            if not chrset:
                chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    @classmethod
    def create_uuid(cls):
        """
        创建随机字符串
        :return:
        """
        text = str(time.time()) + cls.salt(12)
        m = hashlib.md5()
        m.update(bytes(text.encode(encoding='utf-8')))
        return m.hexdigest()

    @staticmethod
    def loads_json(json_str):
        try:
            return json.loads(json_str)
        except Exception as e:
            return json_str

    @staticmethod
    def get_pay_type(pay_type):
        """
        获取支付方式字符串
        :param pay_type: 1 支付宝  3 微信  4 积分  5 epayments
        :return: 
        """
        if str(pay_type) in pay_type_dict:
            return pay_type_dict[str(pay_type)]
        else:
            return 'no available pay_type '
