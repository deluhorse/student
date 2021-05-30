# -*- coding:utf-8 -*-

"""
@author: delu
@file: constants.py
@time: 17/4/12 下午2:22
"""


class Constants(object):
    SELLER_TYPE = 'seller'
    BUYER_TYPE = 'buyer'
    PLATFORM_TYPE = 'platform'
    SUPER_ADMIN_TYPE = 'super_admin'
    ADMIN_TYPE = 'admin'

    SCEN_TYPE_WECHAT = 2
    SCEN_TYPE_FLASH_SALE = 10
    SCEN_TYPE_RAIN_CARD = 11

    # 支付
    PAY_TYPE_WECHAT = 3
    PAY_TYPE_ALIPAY = 1
    PAY_TYPE_BONUS = 4
    PAY_TYPE_EPAYMENTS = 5
    PAY_TYPE_PAYPAL = 6
    PAY_TYPE_STRIPE = 7
    PAY_TYPE_DRP_BALANCE = 8
    PAY_SUB_TYPE_WECHAT = 1
    PAY_SUB_TYPE_ALIPAY = 3

    # 2018-08-20 实付支付方式, 曲线救国, 每增加一种实付方式，都要往tuple里加一项
    REAL_PAY_TYPE_LIST = (PAY_TYPE_ALIPAY, PAY_TYPE_WECHAT, PAY_TYPE_EPAYMENTS, PAY_TYPE_PAYPAL, PAY_TYPE_STRIPE, PAY_TYPE_DRP_BALANCE)

    # 订单状态
    # 未支付
    ORDER_WAIT_PAY = 1
    # 未发货
    ORDER_PAY_SUCCESS = 2
    # 已发货
    ORDER_SEND = 3
    # 已收货
    ORDER_RECEIVED = 4
    # 申请售后中
    ORDER_APPLY = 5
    # 已完成
    ORDER_SETTLED = 10
    # 已结束
    ORDER_FINISH = 7
    # 超卖
    ORDER_OVERBUY = 8
    # 已过期
    ORDER_EXPIRE = -1
    # 已关闭
    ORDER_CLOSE = -2

    # 母单状态
    # 未支付
    PARENT_ORDER_WAIT_PAY = 1
    # 正在处理中
    PARENT_ORDER_PROCESSING = 2
    # 已完成
    PARENT_ORDER_FINISH = 3

    # 售后审核状态
    ORDER_APPROVE_NOT_AUTH = 1
    ORDER_APPROVE_SUCCESS = 2
    ORDER_APPROVE_FAIL = -1

    # 售卖渠道
    SALE_CHANNEL = {
        1: '在线商城',
        2: 'raincard'
    }
    # 售卖渠道 官网
    SALE_CHANNEL_WEB = 1
    # 售卖渠道 小程序
    SALE_CHANNEL_MINI_APP = 3
    # 售卖渠道raincard
    SALE_CHANNEL_RAINCARD = 2

    # 营销活动适用范围
    PM_ALL_GOODS = -1
    PM_GOODS = 1
    PM_GOODS_GROUP = 2
    PM_GOODS_CLASS = 3
    PM_BRAND = 4

    PM_COUPON = 'coupon'
    PM_PROMO_CODE = 'promo_code'
    PM_FULL_CUT = 'full_cut'
    PM_PHLIT = 'b_phlit'

    # 购物车选中状态
    # 全部选中
    SHOPPING_CART_SELECT_ALL = -1
    # 全部取消
    SHOPPING_CART_UNSELECT_ALL = -2
    # 收款方式
    # 代收
    DIRECTION_OTHER = 1
    # 自收
    DIRECTION_SELF = 2

    # 发货通知
    SEND_NOTIFY = '1'
    # 订单催付
    NO_PAY_NOTIFY = '2'
    # 付款成功
    PAY_SUCCESS_NOTIFY = '3'
    # 退款成功
    REFUND_SUCCESS_NOTIFY = '4'
    # 退款失败
    REFUND_FAIL_NOTIFY = '5'
    # 售后未通过
    AFTER_SALE_APPLY_FAILED = '6'

    # 微信
    MEDIA_TYPE_WEIXIN = '2'
    # 短信
    MEDIA_TYPE_SMS = '1'
    # 邮件
    MEDIA_TYPE_EMAIL = '3'

    # 资金，收支类型
    # 订单收入
    FM_ORDER_INCOME = 1
    # 订单退款
    FM_ORDER_REFUND = 2

    # 境内仓库id列表
    DOMESTIC_WAREHOUSE_ID_LIST = [0, 1, 2]
    # 境外仓库id列表
    ABROAD_WAREHOUSE_ID_LIST = [3]

    # 订单取消
    # 默认取消原因
    DEFAULT_CANCEL_CODE = 4
    # 平台管理员取消
    PLATFORM_CANCEL = 5

    # 订单退款
    # 未退款
    NOT_REFUND = 0
    # 退款成功
    REFUND_SUCCESS = 1
    # 退款失败
    REFUND_FAIL = 2

    # 商户提现
    # 未审核
    NOT_REVIEW = '0'
    # 审核通过
    REVIEW_SUCCESS = '1'
    # 审核未通过
    REVIEW_FAIL = '2'
    # 转账处理中
    GIRO_PROCESSING = '3'
    # 已转账
    GIRO_SUCCESS = '4'
    # 转账失败
    GIRO_FAIL = '5'

    JSON_HEADERS = {'content-type': 'application/json'}
    FORM_ID_TYPE_APPLY = 'apply'
    FORM_ID_TYPE_COUPON = 'coupon'
    FORM_ID_TYPE_DISTRIBUTOR_COMMISSION_SETTLE = 'distributor_commission_settle'

    # 营销活动状态
    ACTIVITY_OPEN = 1
    ACTIVITY_CLOSE = 0

    # 拼团相关状态
    GROUP_BUY = 'group_buy'
    # 拼团活动 未开始 | 进行中 | 已结束 | 手动结束
    GROUP_BUY_ACTIVITY_NOTSTART = 1
    GROUP_BUY_ACTIVITY_PERSISTING = 2
    GROUP_BUY_ACTIVITY_FINISH = 3
    GROUP_BUY_ACTIVITY_TERMINATE = 4
    # 拼团实例 拼团创建成功订单未生成| 创建中(订单创建成功待付款) | 拼团中 | 拼团成功 | 拼团失败
    GROUP_BUY_INIT = 0
    GROUP_BUY_CREATING = 1
    GROUP_BUY_PERSISTING = 2
    GROUP_BUY_SUCCESS = 3
    GROUP_BUY_FAIL = 4
    # 拼团活动种类
    # 普通团
    GROUP_BUY_NORMAL = 1
    # 新人团
    GROUP_BUY_NEWBIE = 2

    DATA_SOURCE_CACHE = 'cache'
    DATA_SOURCE_DB = 'db'

    # 已过期
    ACTIVITY_STATUS_EXPIRE = 3
    # 进行中
    ACTIVITY_STATUS_RUNNING = 2
    # 未开始
    ACTIVITY_STATUS_READY = 1

    # 买家余额流水类型
    # 分享得奖励金流水
    BUYER_BALANCE_RECORD_SHARE = '1'
    BUYER_BALANCE_RECORD_REFUND = '2'
    BUYER_BALANCE_RECORD_WITHDRAW = '3'

    # 分销员佣金流水
    DISTRIBUTOR_BALANCE_RECORD_ORDER = '1'
    DISTRIBUTOR_BALANCE_RECORD_REFUND = '2'
    DISTRIBUTOR_BALANCE_RECORD_WITHDRAW = '3'

    # 物流计费方式 1 按件数  2 按重量
    CALCULATE_SHIPPING_FEE_BY_GOODS_NUM = 1
    CALCULATE_SHIPPING_FEE_BY_GOODS_WEIGHT = 2

    # 积分相关常量,z用于活动排序
    BONUS_PAY = 'w_bonus_pay'
    # 积分变动原因
    BONUS_ORDER_DISCOUNT = 1        # 下单抵扣
    BONUS_ORDER_PRESENT = 2         # 下单赚取
    BONUS_MANUALLY_INCREASE = 3     # 人工添加
    BONUS_MANUALLY_DECREASE = 4     # 人工扣除
    BONUS_ACTIVATE_PRESENT = 5     # 激活赠送
    BONUS_REFUND_RETURN = 6         # 售后返还
    BONUS_TIMEOUT_RETURN = 7        # 过期返还

    # 会员卡激活状态 card_status 1、待审核 2、审核成功 3、审核失败
    MEMBER_CARD_WAIT_ACTIVATE = 0
    MEMBER_CARD_ACTIVATED = 1
    MEMBER_CARD_ACTIVATE_FAIL = 2

    # 会员性别 sex
    UNKNOWN_MEMBER = -1
    MALE_MEMBER = 1
    FEMALE_MEMBER = 2

    # 是否代收
    SETTING_TYPE_IS_SELF_PAY = 'is_self_pay'
    # philips会员来源
    SETTING_TYPE_PHILIPS_SOURCE = 'philips_source'

    SHOP_SETTING_TYPE_DICT = {
        'ID_CARD': 'is_need_id_card'
    }

    # 订单类型  1 正常订单  2 拼团订单
    BAOZUN_ORDER_TYPE_NORMAL = 1
    BAOZUN_ORDER_TYPE_GROUPBUY = 2

    # 取消订单类型  9  手动取消  10  系统自动取消
    ORDER_CANCEL_TYPE_MEMBER = 9
    ORDER_CANCEL_TYPE_AUTO = 10

    # 商品库存同步 1 . 同步中  2. 同步完成
    STOCK_STATUS_RUNNING = 1
    STOCK_STATUS_FINISH = 2

    # 分销员审核状态
    # 未审核
    DISTRIBUTOR_APPLY_STATUS_APPLYING = 0
    # 成功
    DISTRIBUTOR_APPLY_STATUS_SUCCESS = 1
    # 失败
    DISTRIBUTOR_APPLY_STATUS_FAIL = 2

    # 分销员资金流水类型
    DISTRIBUTOR_FLOW_TYPE_ORDER_PAY = 'order_pay'
    DISTRIBUTOR_FLOW_TYPE_ORDER_REFUND = 'order_refund'
