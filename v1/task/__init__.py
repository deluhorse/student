# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: __init__.py
@time: 2018/6/5 10:59
"""
import json

from tools.logs import Logs
from tools.date_json_encoder import CJsonEncoder
from tools.date_utils import DateUtils
from source.async_redis import AsyncRedis
# from source.redisbase import RedisBase
from source.properties import Properties
from .report import Report
import sys
import traceback

logger = Logs().logger
properties = Properties('task')
redis = AsyncRedis()
date_utils = DateUtils()

task_queue = properties.get('cache', 'task_queue')
failed_queue = properties.get('cache', 'failed_queue')
loop_num = int(properties.get('task', 'task_num'))


async def add(path='', method='', arguments=None, is_priority=False, sub_task=None):
    """
    添加任务
    :param path: 调用包文件路径
    :param method:  调用方法
    :param arguments: 请求参数
    :param is_priority: 是否优先处理(True or False)
    :param sub_task: 是否有子任务
            sub_task['queue_key'] 目标队列key
            sub_task['task_num'] 任务数
    :return:
    """
    if (path and method and arguments) or sub_task:
        params = {
            'path': path,
            'method': method,
            'arguments': arguments,
            'sub_task': sub_task
        }

        try:
            params = json.dumps(params, cls=CJsonEncoder)
            if is_priority:
                await redis.rpush(task_queue, params)
            else:
                await redis.lpush(task_queue, params)
        except Exception as e:
            await Report.report('添加任务异常', e)


async def get_one(task_queue_key=None):
    """
    从队列里获取一条数据
    :param task_queue_key:
    :return:
    """
    result = await redis.rpop(task_queue_key if task_queue_key else task_queue)
    return result


async def save_task_error(task, e):
    """
    保存失败任务信息
    :param task: 任务数据
    :param e: 异常信息
    :return:
    """
    try:
        task = json.loads(task) if isinstance(task, str) else task
        trace = ''.join(traceback.format_exception(*sys.exc_info())[-2:])
        task = json.dumps({
            'task': task,
            'e': trace,
            'time': date_utils.time_now()
        }, cls=CJsonEncoder)
        await redis.lpush(failed_queue, task)
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == '__main__':
    add('goods.stock.service', 'update_sales', {
        "goods_sales": [
            {
                "goods_id": "G009MV3GGO",
                "sku_id": "S00CBJOTHY",
                "sales": -1
            }
        ], "trigger_position": "return_sku_stock"
    })
