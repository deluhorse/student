# -*- coding:utf-8 -*-

"""
@author: delu
@file: service_manager.py
@time: 17/4/18 下午5:21
service 服务模块
"""
import importlib

from v1.conf.remote_controller_config import REMOTE_CONTROLLER
from .system_constants import SystemConstants
from tools.httputils import HttpUtils
from tools.logs import Logs
import time

logger = Logs().logger


class ServiceManager(object):
    # 权限树
    # print CONF['power_tree']
    # power_tree = generate_power_tree()

    @staticmethod
    def do_local_service(service_path, method, params={}, version='', power=[]):
        """
        执行本地服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        start_time = int(1000 * time.time())
        model = importlib.import_module(version + '.module.' + service_path)
        service = model.Service()
        # 将权限树传给ServiceBase的self
        service.power_tree = power

        # # 如果语言不存在，则默认为中文
        # if 'language' not in params or not params['language']:
        #     params['language'] = 'cn'
        # language_module = importlib.import_module('language.' + params['language'])
        # setattr(service, 'language_code', language_module.Code)
        func = getattr(service, method)

        result = func(params)
        cost_time = int(time.time() * 1000) - start_time
        # 发消息记录这些信息
        # log_params = {
        #     'service_path': service_path,
        #     'method': method,
        #     'params': json.dumps(params, cls=CJsonEncoder),
        #     'cost_time': cost_time
        # }
        # if cmp(service_path, 'task.log.method.service') != 0:
        #     redis_conn.lpush('task_data_list', json.dumps({'service_path': 'task.log.method.service',
        #                                                    'method': 'create_log',
        #                                                    'params': log_params}, cls=CJsonEncoder))
        return result

    @staticmethod
    def do_remote_service(url, params, http_type='get'):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        try:
            if http_type == 'post':
                # 发送post请求
                HttpUtils.do_post(url, params)
            else:
                # 发送get请求
                HttpUtils.do_get(url, params)
        except Exception as e:
            logger.exception(e)
            return SystemConstants.REMOTE_SERVICE_ERROR

    @staticmethod
    def do_service(service_path='', method='', params={}, version='', power=[]):
        """
        执行服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        # 判断该服务是否需要远程支持
        if service_path in REMOTE_CONTROLLER and method in REMOTE_CONTROLLER[service_path]:
            url = REMOTE_CONTROLLER['host'] + REMOTE_CONTROLLER[service_path][method][0]
            return ServiceManager.do_remote_service(url, params, http_type=REMOTE_CONTROLLER[service_path][method][1])
        else:
            return ServiceManager.do_local_service(service_path, method, params, version, power)

    @staticmethod
    def get_fun(service_path, method, params, version='v1'):
        """
        根据方法路径获取方法实例
        :param service_path:
        :param method:
        :param params:
        :param version:
        :return:
        """
        model = importlib.import_module(version + '.module.' + service_path)
        service = model.Service()

        # 如果语言不存在，则默认为中文
        if 'language' not in params or not params['language']:
            params['language'] = 'cn'
        language_module = importlib.import_module('language.' + params['language'])
        setattr(service, 'language_code', language_module.Code)
        func = getattr(service, method)
        return func
