# -*- coding:utf-8 -*-

import datetime
import hashlib
import importlib
import json
import random
import time
from functools import wraps

import tornado.escape
import tornado.gen

import conf.config as config
import task
from task import schedule
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.properties import Properties
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_json_encoder import CJsonEncoder
from tools.date_utils import DateUtils
from tools.excel_util import excel_util
from tools.httputils import HttpUtils
from tools.money_utils import MoneyUtils
from tools.logs import Logs
from tools.rsa_utils import RsaUtils
from tools.string_util import StringUtils
from language.manager import LangManager


class ServiceBase(object):
    dicConfig = config.CONF
    time = time
    datetime = datetime
    json = json
    hashlib = hashlib
    constants = Constants
    error_code = Code
    cache_key_predix = CacheKeyPredix
    properties = Properties()
    redis = AsyncRedis()
    httputils = HttpUtils
    date_utils = DateUtils
    common_utils = CommonUtil
    string_utils = StringUtils
    money_utils = MoneyUtils
    date_encoder = CJsonEncoder
    rsa_utils = RsaUtils
    excel_util = excel_util
    logger = Logs().logger
    lang = LangManager()
    power_tree = []
    task = task
    schedule = schedule

    # tornado_redis = TornadoRedis()

    def md5(self, text):
        """
        md5加密
        :param text: 
        :return: 
        """
        result = hashlib.md5(text.encode(encoding='utf-8'))
        return result.hexdigest()

    def sha1(self, text):
        """
        sha1生成签名
        :param text: 
        :return: 
        """
        result = hashlib.sha1(text.encode(encoding='utf-8'))
        return result.hexdigest()

    def import_model(self, model_name):
        """
        加载数据类
        :param model_name: string 数据类名
        :return: 
        """
        try:
            model = importlib.import_module('module.' + model_name)
            return model.Model()
        except Exception as e:
            self.logger.exception(e)
            return None

    def time_to_mktime(self, time_str, format_str):
        """
        将时间字符串转化成时间戳
        :param params: 
        :return: 
        """
        return time.mktime(time.strptime(time_str, format_str))

    def salt(self, salt_len=6, is_num=False, chrset=''):
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

    def create_uuid(self):
        """
        创建随机字符串
        :return: 
        """
        text = str(time.time()) + self.salt(12)
        m = hashlib.md5()
        m.update(bytes(text.encode(encoding='utf-8')))
        return m.hexdigest()

    def loads_list(self, list_str):
        """
        转换字符串成列表
        :param list_str: 
        :return: 
        create:wsy 2017/7/31
        """
        try:
            data_list = self.json.loads(list_str)
        except Exception as e:
            self.logger.exception(e)
            data_list = []
        return data_list

    def loads_dic(self, dic_str):
        """
        转换字符串成字典
        :param dic_str: 
        :return: 
        create:wsy 2017/7/31
        """
        try:
            data_dic = self.json.loads(dic_str)
        except Exception as e:
            self.logger.exception(e)
            data_dic = {}
        return data_dic

    def escape_string(self, data, un=None):
        """
        特殊字符转义
        :param data: string, tuple, list, dict 转义数据
        :param un: 
        :return: 
        """
        if isinstance(data, str):
            return tornado.escape.xhtml_escape(data) if not un else tornado.escape.xhtml_unescape(data)
        elif isinstance(data, tuple) or isinstance(data, list):
            lisData = []
            for item in data:
                lisData.append(
                    tornado.escape.xhtml_escape(str(item)) if not un else tornado.escape.xhtml_unescape(str(item)))

            return lisData
        elif isinstance(data, dict):
            for key in data:
                data[key] = tornado.escape.xhtml_escape(str(data[key])) if not un else tornado.escape.xhtml_unescape(
                    str(data[key]))

            return data

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'],
                                         power=self.power_tree)

    def sign_params(self, params, secret_key):
        """
        验签
        :param params:
        :param secret_key:
        :return:
        """

        params_keys = []
        for (k, v) in params.items():
            if k != 'sign':
                params_keys.append(k)

        params_string = ''
        for key in sorted(params_keys):
            params_string += (key + '=' + params[key] + '&')
        params_string = self.md5(params_string + secret_key).upper()
        return params_string == params['sign'].upper()

    @tornado.gen.coroutine
    def load_extensions(self, trigger_position, data):
        """
        加载扩展程序
        :param trigger_position:
        :param data:
        :return:
        """
        data['trigger_position'] = trigger_position
        result = yield self.do_service('cfg.extensions.service', 'query', {'trigger_position': trigger_position})
        if result and 'code' in result and result['code'] == 0:
            # 发送消息
            for item in result['data']:
                service_path = item['package_path']
                method = item['method']
                # self.publish_message(service_path, method, data)
                yield self.task.add(service_path, method, data)

    def _e(self, error_key):
        """
        :param error_key: 
        :return: 
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        # if error_key in self.language_code:
        #     data['msg'] = self.language_code[error_key]

        return data

    def _gre(self, data):
        """
        tornado.gen.Return
        :rtype:
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(self._e(data))

    def _gree(self, error_key, customer_msg):
        """
        自定义扩展错误信息
        :param error_key: 
        :param customer_msg: 自定义额外错误信息
        :return: 
        """
        result = self._e(error_key)
        if customer_msg:
            result['msg'] += '({})'.format(customer_msg)
        return tornado.gen.Return(result)

    def _grs(self, data={}):
        """
        成功返回
        :param data: 
        :return: 
        """
        result = self._e('SUCCESS')
        result['data'] = data
        return tornado.gen.Return(result)

    def _gr(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(data)

    @tornado.gen.coroutine
    def cache_get(self, key):
        result = yield self.redis.get(key)
        if result:
            expire = yield self.redis.ttl(key)
            if expire < int(self.properties.get('expire', 'CACHE_REFRESH_EXPIRE')):
                yield self.redis.expire(key, self.properties.get('expire', 'CACHE_EXPIRE'))
            try:
                result = json.loads(result)
            except Exception as e:
                yield self.redis.expire(key, 0)
                result = False
            return result
        else:
            return False

    @tornado.gen.coroutine
    def cache_set(self, key, value):
        try:
            value = json.dumps(value, cls=self.date_encoder)
            yield self.redis.set(key, value)
            yield self.redis.expire(key, self.properties.get('expire', 'CACHE_EXPIRE'))
            return True
        except Exception:
            return False

    def get_path(self, data, power_path_list=None):
        """
        1 遍历用户权限树，如果有child，获得child的path，如果没有，返回power['path']
        2 递归的遍历child获得path,直到所有child为空
        3 将所有path加载到power_tree 列表中
        :param data: 用户权限树
        :return:
        """
        if power_path_list is None:
            power_path_list = []
        for power in data:
            power_path_list.append(str(power['path']))
            if power['child']:
                self.get_path(power['child'], power_path_list)
                # else:
                #     power_path_list.append(str(power['path']))
        return power_path_list

    @classmethod
    def params_set(cls, model=None, data=None):
        """
        数据对象设置
        :param model:
        :param data:
        :return:
        """
        def decorate(func):
            @wraps(func)
            @tornado.gen.coroutine
            def wrapper(*args, **kwargs):
                o = args[0]
                params = args[1]
                model_data = None
                if hasattr(o, model):
                    model_obj = getattr(o, model)
                    if hasattr(model_obj, data):
                        model_data = getattr(model_obj, data)

                new_args = args
                if model_data:
                    if isinstance(params, dict):
                        model_data.update(params)
                        new_args = (args[0], model_data)

                result = yield func(*new_args, **kwargs)

                return result

            return wrapper
        return decorate
