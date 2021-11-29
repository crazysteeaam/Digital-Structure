import math
import numpy as np


# 队列ADT
class ArrayQueue:
    DEFAULT_CAPACITY = 2

    def __init__(self):
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise ValueError('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        if self.is_empty():
            raise ValueError('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        if self._size == len(self._data):
            self.resize(2 * len(self._data))
        pos = (self._front + self._size) % len(self._data)
        self._data[pos] = e
        self._size += 1

    def resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0

    def printqueue(self):
        for i in range(self._size):
            pos = (self._front + self._size - 1 - i) % len(self._data)
            #print(str(i), ": ", str(pos))
            print(self._data[pos], end=" ")
        print()


class normal():
    # 门诊函数库
    def normal_number(normal_loc, normal_scale):
        # 生成每分钟门诊病人到达人数
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
        # 计算门诊要服务的总用户人数
        for numsum in range(sum_time):
            normal_perminnumber = normal.normal_number(
                normal_loc, normal_scale)
            normal_queuenumber.append(normal_perminnumber)
        normal_sumlist = 0
        for normalsumlist in range(len(normal_queuenumber)):
            normal_sumlist = normal_sumlist+normal_queuenumber[normalsumlist]
        return normal_sumlist

    def normal_get_patientNO(self, current_time):
        # 用户挂号成功，成功进入排队队列
        global normal_patientnumber
        normal_i = 0
        while normal_i < normal_queuenumber[current_time]:
            normal_patientnumber = normal_patientnumber+1
            normal_i = normal_i+1
            ArrayQueue.enqueue(normal_queue, "N"+str(normal_patientnumber))

    def normal_dequeue(self):
        # 模拟门诊排队队列出队过程
        global normal_group
        if normal_group <= ArrayQueue.__len__(self):
            for normalgroupnumber in range(normal_group):
                ArrayQueue.dequeue(self)
        else:
            while ArrayQueue.__len__(self):
                ArrayQueue.dequeue(self)


class main():
    global sum_time, normal_loc, normal_scale, normal_sumlist, current_time, normal_patientnumber, normal_group  # 定义全局变量
    global normal_queuenumber, normal_queue  # 定义全局顺序表、队列

    # 输入
    sum_time = int(input("请输入总时间（单位：分钟）："))
    normal_loc = float(input("请输入每分钟门诊病人到达人数正态分布的均值："))
    normal_scale = float(input("请输入每分钟门诊病人到达人数正态分布的标准差："))
    normal_group = int(input("请输入服务门诊病人的窗口总数："))

    normal_queuenumber = list()
    normal_sumlist = normal.sum_normalpatient(sum_time)
    print("门诊要服务的总用户人数为%d" % (normal_sumlist))
    normal_queue = ArrayQueue()
    current_time = 0
    normal_patientnumber = 0

    while current_time < sum_time:
        normal.normal_get_patientNO(normal_queue, current_time)
        normal.normal_dequeue(normal_queue)
        current_time = current_time+1
    ArrayQueue.printqueue(normal_queue)
    print()
    print("经过%d分钟，门诊病人完成诊疗人数为%d人" %
          (sum_time, int(normal_sumlist)-int(ArrayQueue.__len__(normal_queue))))
    print("门诊病人剩下人数为%d" % (ArrayQueue.__len__(normal_queue)))
