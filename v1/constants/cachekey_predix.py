# -*- coding:utf-8 -*-

"""
@author: delu
@file: cachekey_predix.py
@time: 17/4/13 下午3:01
"""


class CacheKeyPredix(object):

    # 用户管理

    # 管理员分组id
    GROUP_ID = 'group_id'
    # 管理员账户id
    ACCOUNT_ID = 'account_id'
    # 管理员id
    ADMIN_ID = 'admin_id'
    # 管理员id
    UID = 'uid'
    # 店铺id
    SHOP_ID = 'shop_id'
    # 店铺ID和二级域名映射
    DOMAIN_SHOP_ID = 'shop:domain:'
    # 店铺基本信息
    SHOP_INFO = 'shop:info:'
    # 店铺有效期信息
    SHOP_VALIDITY_INFO = 'shop:validity:'
    # 店铺配置信息
    SHOP_SETTING = 'shop:setting:'
    # 平台管理员token前缀
    SUPERADMIN_TOKEN = 'superadmin_token_'
    # 管理员token前缀
    ADMIN_TOKEN = 'admin_token_'
    # 买家token前缀
    BUYER_TOKEN = 'buyer_token_'
    # 平台授权token
    PLATFORM_TOKEN = 'token:platform:'

    # 买家地址编号
    BUYER_ADDR_NO = 'buyer_addr_no'
    # 买家id
    BUYER_ID = 'buyer_id'
    # 微信小程序 - code
    MINI_APP_CODE = 'mini_app_code_'
    # 商品SKU库存
    GOODS_SKU_STOCK = 'sku:stock:'
    # 订单基础id，用于生成订单号
    ORDER_BASE_ID = 'order_base_id'
    # 退款批次号基础no,用于生成退款批次号
    BATCH_BASE_NO = 'batch_base_no'
    # 微信小程序，模板消息发送队列
    MINI_APP_MODEL_MESSAGE_USER = 'mini_app_model_message_user_'
    # 微信小程序access_token
    MINI_APP_ACCESS_TOKEN = 'mini_app_access_token'
    # 物流模板编号
    GOODS_FARETMPLT_NO = 'goods_faretmplt_no'
    # 微信token
    WECHAT_ACCESS_TOKEN = 'wechat_access_token'
    # 微信jsapi信息
    WECHAT_JSAPI = 'wechat_jsapi'
    # 微信jsapi_ticket
    WECHAT_JSAPI_TICKET = 'wechat_jsapi_ticket'
    # 微信小程序基本信息
    MINI_APP_INFO = 'mini_app_info_'
    # 微信小程序id关联的shop
    MINI_APP_ID_TO_SHOP_ID = 'mini_app_id_to_shop_id_'
    MINI_APP_USER_NAME = 'mini_app_user_name_'
    # 保存每个店铺小程序审核信息,如果已经成功发布了一次,则删除
    MINI_APP_AUDIT_INFO = 'mini_app_audit_info_'
    # 保存审核时间
    MINI_APP_AUDIT_TIME = 'mini_app_audit_time_'
    # 店铺小程序模板
    SHOP_MINI_APP_MODEL_MESSAGE = 'shop:mini:app:model:message:'
    # ticket
    TICKET = 'ticket'
    # component_access_token
    COMPONENT_ACCESS_TOKEN = 'component_access_token'
    # 修改库存销量
    UPDATE_STOCK_SALE = 'update_stock_sale'
    # 临时page_id
    TEMP_PAGE_ID = 'temp_page_id'
    # 任务
    TASK_DATA_LIST = 'task_data_list'
    # 失败任务队列
    ERROR_TASK_DATA_LIST = 'error_task_data_list'
    # 营销活动前缀
    PM = 'pm_'
    # 优惠券库存
    PM_COUPON_STOCK = 'coupon:stock:'
    # 全部商品
    PM_ALL_GOODS = 'pm_all_goods'
    # 买家已领取的优惠券数量
    BUYERWALLET = 'buyerwallet_'
    # 买家参与的优惠券活动
    ALL_BUYERWALLET = 'all_buyerwallet_'
    # 订单支付缓存
    ORDER_PAY = 'order_pay_'
    # 充值订单支付缓存
    PAY_RECORD = 'pay_record_'
    # 订单支付回调缓存
    ORDER_NOTIFY = 'order_notify_'
    # 定时任务订单过期
    SCHEDULE_ORDER_EXPIRE = 'schedule_order_expire_'
    # 短信定时任务订单过期
    ORDER_SMS_NOTIFY_EXPIRE = 'order_sms_notify_expire_'
    # 微信定时任务订单过期
    ORDER_WECHAT_NOTIFY_EXPIRE = 'order_wechat_notify_expire_'
    # 小程序定时任务订单过期消息通知
    ORDER_MINI_APP_NOTIFY_EXPIRE = 'order:mini:app:notify:expire:'
    # 定时任务订单过期消息通知
    ORDER_NOTIFY_EXPIRE = 'order:notify:expire:'
    # 验证码
    VERIFY_CODE = 'verify:code:'
    # 充值短信条数
    SMS_BALANCE = 'sms:balance:'
    # 商品基本信息
    GOODS_INFO = 'goods:info:'
    # 商品所有SKU
    GOODS_SKU_ALL = 'goods:sku:all:'
    # 商品所属分组
    GOODS_GROUP = 'goods:group:'
    # SKU信息，包含GOODS信息
    SKU_INFO = 'sku:info:'
    # 分组树
    GROUP_TREE = 'group_tree:'
    # 分组的子分组id集合缓存,hashmap，结构为group_id --> [child_group_id_list]
    CHILD_GROUP_ID_LIST = 'child_group_id_list:'
    # 店铺支付参数
    SHOP_PAYMENT = 'shop_payment_'
    # 店铺管理员配置
    ADMIN_CONFIG = 'admin_config_'
    # 税率缓存
    HSCODE = 'hscode_'

    # 商品信息md5,更新商品时先去缓存比对
    GOODS_MD5 = 'goods_md5_'
    # 发送给osm的订单队列
    OMS_SALES_ORDER = 'oms_sales_order'
    # 发送给osm的用户队列
    OMS_BUYER_INFO = 'oms_buyer_info'
    # 发送给crm的用户队列
    CRM_BUYER_INFO = 'crm_buyer_info'
    # 仓库对应的物流模板
    WAREHOUSE_FARE_TEMPLATE = 'fare_template_'
    # 店铺的物流模板
    SHOP_FARE_TEMPLATE = 'fare_template_'

    # 物流模板对应的物流信息
    FARE = 'fare_'
    # 微信prepay_id缓存, 用于小程序发模板消息
    PREPAY_ID = 'prepay_id_'

    # 拼团活动定时开始
    SCHEDULE_GROUP_BUY_ACTIVITY_START = 'schedule_group_buy_activity_start_'
    # 拼团活动定时结束
    SCHEDULE_GROUP_BUY_ACTIVITY_END = 'schedule_group_buy_activity_end_'
    SCHEDULE_GROUP_BUY_END = 'schedule_group_buy_end_'
    # 拼团活动参加人数记录
    GROUP_BUY_ACTIVITY_PEOPLE_HASH = 'group_buy_activity_people_hash_'
    # 拼团实例人数
    GROUP_BUY_PEOPLE_SET = 'group_buy_people_set_'
    # 拼团机器人
    GROUP_BUY_ROBOT_BUYER_SET = 'group:buy:auto:set:'
    # 拼团订单过期任务(解锁拼团人数)
    GROUP_BUY_ORDER_EXPIRE = 'group_buy_order_expire_'

    # 微信第三方平台授权access_token, 命名方式为 _shopid_type
    WECHAT_OPEN_ACCESS_TOKEN = 'wechat_open_'

    # 微信卡券api_ticket
    WECHAT_CARD_API_TICKET = 'wechat_card_api_ticket_'

    # 快递100重试次数存储
    LOGIS_SUBSCRIBE_COUNT = 'logis:subscribe:count'

    # paypal token
    PAYPAL_TOKEN = 'paypal:token:'

    # 奖励金手机号cache
    PHLIT_MOBILE = 'phlit:mobile:'

    # 宝尊会员token
    BAOZUN_TOKEN = 'baozun:token:'
    # 宝尊商品库存同步状态 1 同步中 2 同步完成
    BAOZUN_STOCK_UPDATE = 'baozun:stock:'

    # 瓜分券团过期定时任务
    SCHEDULE_DIVIDE_COUPON_GROUP_END = 'schedule_divide_coupon_group_end_'
    # 瓜分券创建次数缓存
    DIVIDE_GROUP_CREATE_COUNT = 'divide_group_create_count_'
    # 瓜分券活动没人参加次数缓存
    DIVIDE_COUPON_ACTIVITY_PEOPLE_HASH = 'divide_coupon_activity_people_hash_'
    # 瓜分团参与用户
    DIVIDE_GROUP_PEOPLE_SET = 'divide_group_people_set_'
    # 分销员可用余额缓存
    DISTRIBUTOR_AVAILABLE_BALANCE = 'distributor:available:balance:'
    # 分销员可用推广费缓存
    DISTRIBUTOR_AVAILABLE_PROMOTION = 'distributor:available:promotion'

