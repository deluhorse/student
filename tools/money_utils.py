# coding: utf-8
"""
@author: xly
@file: money_utils
@time: 2018/5/30 下午4:34

"""


class MoneyUtils(object):

    @staticmethod
    def to_cent(value, is_cent=False):
        """
        把金额转化为分
        :param value: 需要转化的值
        :param is_cent: 值的单位 元／分
        :return:
        """
        # 转化成字符来计算
        if not isinstance(value, str):
            value = str(value)
        num = 0
        if value:
            if is_cent:
                return int(value.split('.')[0])
            else:
                num_list = value.split('.')
                num += int(num_list[0]) * 100
                if len(num_list) >= 2:
                    deci = num_list[1] + '00'
                    deci = deci[0: 2]
                    num += int(deci)
            return num
        return False

    @staticmethod
    def to_yuan(value, is_cent=False):
        """
        把金额转化成元(返回字符串)
        :param value: 需要转化的值
        :param is_cent: 值的单位 元／分
        :return:
        """
        if is_cent:
            temp_str = '00' + str(value)
            temp_str = temp_str[:-2] + '.' + temp_str[-2:]
            zero_index = 0
            for i in range(len(temp_str)):
                if temp_str[i] == '0' and temp_str[i+1] != '.':
                    zero_index = i + 1
                else:
                    break
            res = temp_str[zero_index:]

        else:
            # 暂时不需要
            res = None
        return res


if __name__ == '__main__':
    s = MoneyUtils()
    # print s.money2int(1.134, to_cent=False)
    # print(s.to_cent('12'))
    # print(s.to_cent('12.3'))
    # print(s.to_cent('12.34'))
    # print(s.to_cent('12.345'))
    # print(s.to_cent(12))
    # print(s.to_cent(12.3))
    # print(s.to_cent(12.34))
    # print(s.to_cent(12.345))
    # print(s.to_cent(12.345, True))
    # print(s.to_cent('12.345', True))
    # print(s.to_cent(12345, True))
    # print(s.to_cent('12345', True))

    print(s.to_yuan(1, True))
    print(s.to_yuan(10, True))
    print(s.to_yuan(101, True))
