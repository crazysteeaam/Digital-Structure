import math
import numpy as np


class normal():
    def normal_number(normal_loc, normal_scale):
        """
        :param normal_loc: 门诊病人到达人数正态分布的均值
        :param normal_scale: 门诊病人到达人数正态分布的标准差
        :return:从正态分布中产生的随机数
        """
        # 正态分布中的随机数生成
        number = math.floor(np.random.normal(
            loc=normal_loc, scale=normal_scale))
        # 返回值
        return number

    def sum_normalpatient(sum_time):
        for numsum in range(sum_time):
            normal_perminnumber = normal.normal_number(
                normal_loc, normal_scale)
            normal_queuenumber.append(normal_perminnumber)
        normal_sumlist = 0
        for normalsumlist in range(len(normal_queuenumber)):
            normal_sumlist = normal_sumlist+normal_queuenumber[normalsumlist]
        print("门诊要服务的总用户人数为%d" % (normal_sumlist))


class main():
    global sum_time, normal_loc, normal_scale, normal_sumlist
    global normal_queuenumber
    sum_time = int(input("请输入总时间："))
    normal_loc = float(input("请输入门诊病人到达人数正态分布的均值："))
    normal_scale = float(input("请输入门诊病人到达人数正态分布的标准差："))
    normal_queuenumber = list()
    normal.sum_normalpatient(sum_time)
