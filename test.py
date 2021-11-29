import math
import numpy as np
import pandas as pd
import pymysql
import matplotlib.pyplot
from sqlalchemy import types
from sqlalchemy.types import VARCHAR


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


class alluse():
    def averagewaittime():
        # 计算所有病人平均等待时间
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")
        cursor = db.cursor()
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) AS waittimelength FROM waittime"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        results = cursor.fetchone()
        db.close()  # 最后关闭连接
        return results


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
        global normal_patientnumber, patientinf
        normal_i = 0
        while normal_i < normal_queuenumber[current_time]:
            normal_patientnumber = normal_patientnumber+1
            normal_i = normal_i+1
            ArrayQueue.enqueue(normal_queue, normal_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """insert into waittime(patientinfo,entertime) values(%d,%d)""" % (
                normal_patientnumber, current_time)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()  # 事务代码
            except Exception as e:
                print("添加失败", e)
                db.rollback()  # 发生错误 回滚事务
            db.close()  # 最后关闭连接

    def normal_dequeue(self):
        # 模拟门诊排队队列出队过程
        global normal_group
        if normal_group <= ArrayQueue.__len__(self):
            for normalgroupnumber in range(normal_group):
                patientinf = ArrayQueue.first(self)
                ArrayQueue.dequeue(self)
                db = pymysql.connect(
                    host="localhost", user="root", password="Qqhh12345", database="ymyhospital", charset="utf8")
                cursor = db.cursor()
                sql = """update waittime set exittime=%d where patientinfo=%d""" % (
                    current_time, patientinf)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()  # 事务代码
                except Exception as e:
                    print("添加失败", e)
                    db.rollback()  # 发生错误 回滚事务
                db.close()  # 最后关闭连接
        else:
            while ArrayQueue.__len__(self):
                ArrayQueue.dequeue(self)


class main():
    db_info = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Qqhh12345',
        'database': 'ymyhospital',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**db_info)
    cursor = conn.cursor()

    global sum_time, normal_loc, normal_scale, normal_sumlist, current_time, normal_patientnumber, normal_group, average_waittime  # 定义全局变量
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
    normal_patientnumber = 10000

    while current_time < sum_time:
        normal.normal_get_patientNO(normal_queue, current_time)
        normal.normal_dequeue(normal_queue)
        current_time = current_time+1
    ArrayQueue.printqueue(normal_queue)
    print()
    print("经过%d分钟，门诊病人完成诊疗人数为%d人" %
          (sum_time, int(normal_sumlist)-int(ArrayQueue.__len__(normal_queue))))
    print("门诊病人剩下人数为%d人" % (ArrayQueue.__len__(normal_queue)))
    average_waittime = alluse.averagewaittime()
    print("所有病人的平均等待时间为%f分钟" % (average_waittime))
