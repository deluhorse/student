#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import os
import random
import re
import time

import tornado.gen

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.controller import Controller
from source.properties import Properties
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.date_json_encoder import CJsonEncoder
from tools.logs import Logs


class Base(Controller):

    json = json
    time = time
    logged_user = {}
    # redis = RedisBase()
    redis = AsyncRedis()
    user_data = {}
    buyer_user_data = {}
    version = config.CONF['version']
    cache_key_pre = CacheKeyPredix
    error_code = Code
    constants = Constants
    properties = Properties()
    logger = Logs().logger
    auth = None
    shop_id = '0'
    _params = {}
    power_tree = []

    # def initialize(self):
    #     """
    #     初始化
    #     初始化数据类
    #     """
    #     # Controller.config = config.CONF
    #     # Controller.initialize(self)
    #     # # self.view_data['title'] = self.config['title']
    #     # # 访问者身份标识
    #     # self.get_user_unique_code()
    #     # self._params = self.get_params()

    @tornado.gen.coroutine
    def prepare(self):
        """
        接受请求前置方法
            1.解析域名
            2.检查IP限制
            3.权限检查
        :return:
        """
        # 访问者身份标识
        self.get_user_unique_code()
        self._params = self.get_params()

        # user_data_dict = yield self.__get_login_user_data()
        # # 1.
        # yield self.get_shop_host(self.request.host)

        # 2.检查IP限制
        # intercept_status = yield self.intercept_ip(user_data_dict)
        # if not intercept_status:
        #     self.finish()

        # 3.
        if self.auth:
            if self.auth[0] is not None:
                auth_status = yield self.auth_check(user_data_dict)
                if not auth_status:
                    self.finish()

                # 刷新token
                yield self.refresh_token()

    @tornado.gen.coroutine
    def intercept_ip(self, user_data_dict):
        """
        拦截IP 对C端拦截，B端不拦截
            1. 检查登录用户信息，如果有商户信息，所有请求不检查IP拦截
            2. 调用服务计算拦截
        :return:
        """
        # 判断是否有seller信息，如果有不检查IP
        seller_data = user_data_dict.get('seller', {})
        if seller_data:
            raise self._gr(True)

        # 调用IP拦截service
        result = yield self.do_service('system.ip_country.service', 'intercept', {
            'shop_id': self._params.get('shop_id', ''),
            'ip': self.request.remote_ip
        })

        if result['code'] != 0:
            self.error_out(result)
            raise self._gr(False)

        raise self._gr(True)

    @tornado.gen.coroutine
    def auth_check(self, user_data_dict):
        """
        登录认证
            根据控制器的权限设置，调用不同的权限检查
        """
        # # 1.获取登录用户信息
        # user_data_dict = yield self.__get_login_user_data()

        auth = self.auth
        # 如果没有设置权限，返回
        if not auth or not auth[0]:
            raise self._gr(True)

        is_auth_error = False
        is_login = True
        is_auth = True
        power_group = auth[0]
        no_check_control = auth[1] if len(auth) > 1 else False
        # 2.根据控制器设置，进行检查
        for group in power_group:
            if group == 'buyer':
                # 买家
                user_data = user_data_dict.get('buyer', {})
                if user_data:
                    if 'user_type' not in user_data:
                        is_login = False
                        continue

                    if user_data['user_type'] not in self.auth[0]:
                        is_auth = False
                        continue

                    # 判断是否开始平台化，如果未开始，执行店铺检查
                    is_platform = self.properties.get('base', 'IS_PLATFORM')
                    if is_platform == 'False' and str(user_data.get('shop_id', '0')) != str(self.params('shop_id')):
                        is_login = False
                        continue
                    is_login = True
                    is_auth = True
                    break
                else:
                    is_login = False
                    continue

            elif group == 'admin' or group == 'seller':
                # 商户
                user_data = user_data_dict.get('seller', {})
                if not user_data:
                    is_login = False
                    continue

                if 'user_type' not in user_data:
                    is_login = False
                    continue
                if user_data['user_type'] not in self.auth[0]:
                    is_auth = False
                    continue

                check_power_result = yield self.__check_power(user_data, no_check_control)
                if not check_power_result:
                    raise self._gr(False)
                is_login = True
                is_auth = True
                break

            elif group == 'platform':
                # 三方平台
                user_data = yield self.sign_auth_platform()
                if not user_data:
                    is_auth = False
                    continue
                if 'user_type' not in user_data:
                    is_login = False
                    continue
                if user_data['user_type'] not in self.auth[0]:
                    is_auth = False
                    continue

                self.user_data = user_data
                is_login = True
                is_auth = True
                break
            else:
                is_auth_error = True
                self.logger.exception('auth error')
                break

        if is_auth_error:
            self.error_out(self._e('AUTH_SET_ERROR'))
            raise self._gr(False)

        if not is_login:
            self.error_out(self._e('NOT_LOGIN'))
            raise self._gr(False)

        if not is_auth:
            self.error_out(self._e('AUTH_ERROR'))
            raise self._gr(False)

        raise self._gr(True)

    @tornado.gen.coroutine
    def __get_login_user_data(self):
        """
        获取用户的登录信息
        :return:
        """
        result = {}
        # 买家
        buyer_token = self.params('buyer_token') if self.params('buyer_token') else self.get_cookie('buyer_token')
        if buyer_token:
            cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(buyer_token)
            user_data = yield self.redis.hgetall(cache_key)
            self.buyer_user_data = user_data
            result['buyer'] = user_data

        # 商户
        sign = self.params('sign')
        if sign:
            sign_token = yield self.sign_login()
            if not sign_token:
                token = self.params('token') if self.params('token') else self.get_cookie('token')
            else:
                token = sign_token
        else:
            token = self.params('token')
            if not token:
                token = self.get_cookie('token')

        if token:
            cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
            user_data = yield self.redis.hgetall(cache_key)
            self.user_data = user_data
            result['seller'] = user_data

        raise self._gr(result)

    @tornado.gen.coroutine
    def __check_power(self, user_data, no_check_control):
        """
        检查权限
        :param user_data:
        :param no_check_control:
        :return:
        """
        # 1 获取店铺权限
        # 2 group_id=0 超级管理员,查看用户请求power是否符合店铺权限
        # 3 group_id>0 普通管理员,查看用户请求power是否符合普通用户权限(shop_id)
        if not no_check_control:
            # 获取前端请求uri，替换api全段字段，用户请求权限
            base_url_prefix = self.properties.get('base', 'BASE_URL_PREFIX')\
                .replace('BASE_URL_PREFIX=', '').replace('\n', '')
            power = self.request.uri.replace(base_url_prefix, '')
            if 'group_id' in user_data and int(user_data['group_id']) >= 0:
                auth_error_flag = True

                # 管理员menu(每个用户真正的权限树,不管是超级管理员，还是普通管理员)
                menu_params = {
                    'shop_id': user_data['shop_id'],
                    'group_id': user_data['group_id'],
                }
                menu_result = yield self.do_service('user.auth.menu.service', 'query_menu', params=menu_params)
                if menu_result['code'] != 0:
                    raise self._gr(menu_result)
                shop_power = self.get_path(menu_result['data'])

                # 检查请求url的power是否匹配用户权限树shop_power
                for power_tree in shop_power:
                    # 用shop_power 匹配 power
                    # shop_power: /user/auth/power
                    # power: /user/auth/power/query
                    pattern = re.compile(power_tree)
                    if pattern.match(power):
                        auth_error_flag = False
                        break
                # 检查权限
                if auth_error_flag:
                    self.error_out(self._e('AUTH_ERROR'))
                    raise self._gr(False)
            else:
                self.error_out(self._e('AUTH_ERROR'))
                raise self._gr(False)

        raise self._gr(True)

    @tornado.gen.coroutine
    def create_token(self, params, user_type, expire=None):
        """
        创建token和cookie
        :param params:
        :param user_type:
        :param expire:
        :return:
        """
        if not user_type:
            raise self._gr({'code': -1, 'msg': ''})

        # 处理domain
        request = self.request
        host = request.host
        host_port = host.split(':')
        hosts = host_port[0].split('.')

        if self.properties.get('domain', 'base'):
            domain_base = self.properties.get('domain', 'base')
        else:
            domain_base = '.'.join(hosts[-2:])

        # 根据用户类型，生成缓存KEY
        if user_type == 'admin':
            token = self.cache_key_pre.ADMIN_TOKEN + self.salt(salt_len=32)
            cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
            expire = expire if expire else int(self.properties.get('expire', 'ADMIN_EXPIRE'))
            cookie_key = 'token'
            params['user_type'] = self.constants.ADMIN_TYPE
        elif user_type == 'buyer':
            token = self.cache_key_pre.BUYER_TOKEN + self.salt(salt_len=32)
            cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(token)
            expire = expire if expire else int(self.properties.get('expire', 'BUYER_EXPIRE'))
            cookie_key = 'buyer_token'
            params['user_type'] = self.constants.BUYER_TYPE
        else:
            raise self._gr({'code': -1, 'msg': ''})

        # 创建缓存
        yield self.redis.hmset(cache_key, params)

        # 设置cookie
        if 'remember' in params and params['remember'] == '1':
            yield self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
            self.set_cookie(cookie_key, token,
                            expires=time.time() + int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')),
                            domain=domain_base)
        else:
            yield self.redis.expire(cache_key, expire)
            self.set_cookie(cookie_key, token, domain=domain_base)

        raise self._gr({'code': 0,'token': token})

    @tornado.gen.coroutine
    def refresh_token(self):
        """
        刷新token
        :return:
        """
        auth = self.auth
        # 如果没有设置权限，返回
        if not auth or not auth[0]:
            raise self._gr(True)

        power_group = auth[0]
        for group in power_group:
            if group == 'buyer':
                # 买家
                buyer_token = self.params('buyer_token')
                if not buyer_token:
                    buyer_token = self.get_cookie('buyer_token')

                if not buyer_token:
                    continue

                cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(buyer_token)
                expire = int(self.properties.get('expire', 'BUYER_EXPIRE'))
                refresh_expire = int(self.properties.get('expire', 'BUYER_REFRESH_EXPIRE'))

                self.__refresh_token_update(cache_key, expire, refresh_expire)

            elif group == 'admin' or group == 'seller':
                token = self.params('token')
                if not token:
                    token = self.get_cookie('token')

                if not token:
                    continue

                if self.params('sign'):
                    shop_id = self.params('shop_id')
                    token = 'sign:' + shop_id

                cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
                expire = int(self.properties.get('expire', 'ADMIN_EXPIRE'))
                refresh_expire = int(self.properties.get('expire', 'ADMIN_REFRESH_EXPIRE'))

                self.__refresh_token_update(cache_key, expire, refresh_expire)

    @tornado.gen.coroutine
    def __refresh_token_update(self, cache_key, expire, refresh_expire):
        """
        更新token有效期
        :param cache_key:
        :param expire:
        :param refresh_expire:
        :return:
        """
        if cache_key and expire and refresh_expire:
            cache_data = yield self.redis.ttl(cache_key)
            if cache_data:
                left_seconds = int(cache_data)
                # 获取用户登录数据
                # self.user_data = yield self.redis.hgetall(cache_key)
                if (expire - left_seconds) >= refresh_expire:
                    # 如果token的总生命秒数 － 剩余生命秒数 >= 刷新秒数，则重新设置token的生命秒数
                    yield self.redis.expire(cache_key, expire)

    @tornado.gen.coroutine
    def sign_login(self):
        """
        签名登录
            1.验签
            2.验签通过，检查缓存是否有值 ，有值 直接返回真
            3.如果没值，生成缓存
        :return:
        """
        # 验签
        sign = self.params('sign')
        sing_result = yield self.do_service('user.auth.sign.service', 'sign_login', self.params())
        if sing_result['code'] != 0:
            raise self._gr(False)

        # 检查缓存是否有值
        shop_id = self.params('shop_id')
        token = 'sign:' + shop_id
        cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
        user_data = yield self.redis.hgetall(cache_key)
        if user_data:
            raise self._gr(token)

        # 创建缓存
        yield self.redis.hmset(cache_key, {
            'shop_id': shop_id,
            'user_type': self.constants.SELLER_TYPE,
            'admin_id': -1,
            'group_id': 0
        })

        # 设置cookie
        expire = int(self.properties.get('expire', 'ADMIN_EXPIRE'))
        yield self.redis.expire(cache_key, expire)

        raise self._gr(token)

    @tornado.gen.coroutine
    def sign_auth_platform(self):
        """
        平台授权认证
            1.检查token参数，如果有token，根据token获取缓存数据，没有token或缓存数据不存在，进行验签
            2.验签，检查sign参数，如果没有，返回授权失败，有，进行验签
            3.创建登录缓存，返回登录信息及token
        :return:
        """
        # 1.
        token = self.params('token')
        if token:
            cache_key = self.cache_key_pre.PLATFORM_TOKEN + token
            user_data = yield self.redis.hgetall(cache_key)
            if user_data:
                raise self._gr(user_data)

        # 2.
        # psign 为 platform 验签的 sign
        psign = self.params('psign')
        if not psign:
            raise self._gr(False)

        sing_result = yield self.do_service('user.auth.sign.service', 'sign_auth_platform', self.params())
        if sing_result['code'] != 0:
            raise self._gr(False)

        # 3.
        app_id = self.params('app_id')
        token = self.md5('sign:' + app_id)
        cache_key = self.cache_key_pre.PLATFORM_TOKEN + token
        user_data = {
            'app_id': app_id,
            'user_type': self.constants.PLATFORM_TYPE,
            'token': token,
            'admin_id': -1,
            'shop_id': app_id
        }
        yield self.redis.hmset(cache_key, user_data)

        expire = int(self.properties.get('expire', 'ADMIN_EXPIRE'))
        yield self.redis.expire(cache_key, expire)

        raise self._gr(user_data)

    @tornado.gen.coroutine
    def get_user_data(self):
        user_data = None
        params = self.params()

        if self.get_cookie('buyer_token'):
            cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(self.get_cookie('buyer_token'))
            user_data = yield self.redis.hgetall(cache_key)

        elif self.get_cookie('token'):
            cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(self.get_cookie('token'))
            user_data = yield self.redis.hgetall(cache_key)

        if 'sign' in params:
            user_data = yield self.sign_auth_platform()
        raise self._gr(user_data)

    def md5(self, text):
        """ 
        MD5加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        result = hashlib.md5(text.encode('utf-8'))
        return result.hexdigest()

    def create_uuid(self):
        """
        声称随机字符串
        :return: 
        """
        m = hashlib.md5()
        m.update(bytes(str(time.time()), encoding='utf-8'))
        return m.hexdigest()

    def sha1(self, text):
        """ 
        sha1 加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        return hashlib.sha1(text).hexdigest()

    def salt(self, salt_len=6, is_num=False):
        """ 
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    def out(self, data):
        """ 
        输出结果
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))

    def error_out(self, error, data=''):
        """
        错误输出
        :param error: 错误信息对象
        :param data: 返回数据字典
        :return: 
        """
        out = error
        if data:
            out['data'] = data

        self.write(out)

    def clear_template_cache(self):
        """ 清除模板缓存
        """

        self._template_loaders.clear()

    @tornado.gen.coroutine
    def get(self):
        """
        重写父类get方法，接受GET请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    @tornado.gen.coroutine
    def post(self):
        """
        重写父类post方法，接受POST请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    @tornado.gen.coroutine
    def get_shop_host(self, host):
        """
        根据自定义域名/二级域名获取店铺ID
        规则：
            1. 检查访问无名是否为系统域名或其二级域名，是使用二级域名，不是使用自定义域名
            2. 根据二级域名或自定义域名获取店铺ID(有缓存策略)
            3. 将shop_id赋值给上下文对象
        :param host:
        :return:
        """
        is_use_domain = self.properties.get('domain', 'is_use')
        domain_base = self.properties.get('domain', 'base')

        if host and is_use_domain == 'True':
            site_domain = ''
            # 1
            if domain_base in host:
                # site_domain = host
                hosts = host.split('.')
                if len(hosts) > 1 and hosts[0] != 'www' and hosts[0] != 'wxauth' and hosts[0] != 'api':
                    site_domain = hosts[0]
            else:
                # hosts = host.split('.')
                # if len(hosts) > 1 and hosts[0] != 'www' and hosts[0] != 'wxauth' and hosts[0] != 'api':
                #     site_domain = hosts[0]
                hosts = host.split(':')
                site_domain = hosts[0]

            if site_domain:
                # 2
                result = yield self.do_service('channel.shop.service', 'query_shop_domain', {
                    'domain': site_domain
                })
                if result and result['code'] == 0:
                    shop_id = result['data']['shop_id']
                    if shop_id:
                        self.shop_id = shop_id
                        # 给参数对象添加shop_id
                        # params = self.params()
                        # 3
                        self._params['shop_id'] = shop_id

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        language = self.get_cookie('language')
        if not token:
            token = self.params('token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not language:
            language = self.params('language')

        # 从application.settings导入power_tree
        power_tree = self.settings['power_tree']

        # params['token'] = token if token else ''
        # params['buyer_token'] = buyer_token if buyer_token else ''
        # params['language'] = language if language else 'cn'
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'],
                                         power=power_tree)

    def get_user_unique_code(self):
        """
        创建访问者唯一身份标识
        :return:
        """
        cookie_name = 'unique_code'
        unique_code = self.get_cookie(cookie_name)
        if not unique_code:
            unique_code = self.params('unique_code')

        if not unique_code:
            unique_code = self.salt(32)
            self.set_cookie(cookie_name, unique_code)

        return unique_code

    def _e(self, error_key):
        """
        :param error_key:
        :return: 
        """
        # language = self.get_cookie('language')
        # if not language:
        #     language = self.params('language')
        # language = language if language else 'cn'
        # language_module = self.importlib.import_module('language.' + language).Code
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        # if error_key in language_module:
        #     data['msg'] = language_module[error_key]

        return data

    def _gr(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return:
        """
        return tornado.gen.Return(data)

    def params(self, key=''):
        """
        获取参数中指定key的数据
        :param key:
        :return:
        """
        if not key:
            return self._params
        elif key not in self._params:
            return ''
        else:
            return self._params[key]

    def get_user_agent(self):
        """
        获取用户访问数据
        :return:
        """
        request = self.request
        if 'Remote_ip' in request.headers and request.headers['Remote_ip']:
            ip = request.headers['Remote_ip']
        elif 'X-Forward-For' in request.headers and request.headers['X-Forward-For']:
            ip = request.headers['X-Forward-For']
        else:
            ip = request.remote_ip

        cookies = ''
        if request.cookies:
            for k, v in request.cookies.items():
                cookies += k + '=' + v.value + ';'

        try:
            user_agent = request.headers['User-Agent']
        except Exception as e:
            user_agent = ''

        return {
            'user_unique_code': self.get_user_unique_code(),
            'remote_ip': ip,
            'user_agent': user_agent,
            'cookies': cookies
        }

    def get_path(self, data, power_path_list=None):
        """
        1 遍历用户权限树，如果有child，获得child的path，如果没有，返回power['path']
        2 递归的遍历child获得path,直到所有child为空
        3 将所有path加载到power_tree 列表中
        4 获取子路径
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
