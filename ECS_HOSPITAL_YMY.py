import math
import numpy as np
import pandas as pd
import pymysql
import matplotlib.pyplot
import datetime
from sqlalchemy.sql.sqltypes import DateTime

# 获取当前时间戳


class gettime():
    def to_integer(dt_time):
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day

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

# 栈ADT


class ArrayStack(object):

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data.pop()

    def printstack(self):
        for i in range(len(self._data)):
            print(self._data[i], end=' ')
        print()


class alluse():
    def averagewaittime():
        # 计算所有病人平均等待时间
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")
        cursor = db.cursor()
        sql = """UPDATE waittime SET exittime=%d WHERE exittime is NULL""" % (
            sum_time)
        cursor.execute(sql)
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) AS waittimelength FROM waittime WHERE DATE(currentdate) = CURRENT_DATE"""
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


class emergency():
    def emergency_number(emergency_loc, emergency_scale):
        # 生成每分钟急诊病人到达人数
        """
        :param emergency_loc: 急诊病人到达人数正态分布的均值
        :param emergency_scale: 急诊病人到达人数正态分布的标准差
        :return:从正态分布中产生的随机数
        """
        # 正态分布中的随机数生成
        number = math.floor(np.random.normal(
            loc=emergency_loc, scale=emergency_scale))
        # 返回值
        return number

    def sum_emergencypatient(sum_time):
        # 计算急诊要服务的总用户人数
        global emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient
        for enumsum_general in range(sum_time):
            # 计算急诊一般用户每分钟到的人数
            emergency_general_perminnumber = emergency.emergency_number(
                emergency_general_loc, emergency_general_scale)
            if emergency_general_perminnumber < 0:
                emergency_general_perminnumber = 0
            emergency_general_queuenumber.append(
                emergency_general_perminnumber)
        for enumsum_serious in range(sum_time):
            # 计算急诊严重用户每分钟到的人数
            emergency_serious_perminnumber = emergency.emergency_number(
                emergency_serious_loc, emergency_serious_scale)
            if emergency_serious_perminnumber < 0:
                emergency_serious_perminnumber = 0
            emergency_serious_queuenumber.append(
                emergency_serious_perminnumber)
        for enumsum_critical in range(sum_time):
            # 计算急诊危重用户每分钟到的人数
            emergency_critical_perminnumber = emergency.emergency_number(
                emergency_critical_loc, emergency_critical_scale)
            if emergency_critical_perminnumber < 0:
                emergency_critical_perminnumber = 0
            emergency_critical_queuenumber.append(
                emergency_critical_perminnumber)
        emergency_sumlist = 0
        for emergencysumlist1 in range(len(emergency_general_queuenumber)):
            emergency_sumlist = emergency_sumlist + \
                emergency_general_queuenumber[emergencysumlist1]
        emergency_general_sumpatient = emergency_sumlist
        for emergencysumlist2 in range(len(emergency_serious_queuenumber)):
            emergency_sumlist = emergency_sumlist + \
                emergency_serious_queuenumber[emergencysumlist2]
        emergency_serious_sumpatient = emergency_sumlist-emergency_general_sumpatient
        for emergencysumlist3 in range(len(emergency_critical_queuenumber)):
            emergency_sumlist = emergency_sumlist + \
                emergency_critical_queuenumber[emergencysumlist3]
        emergency_critical_sumpatient = emergency_sumlist - \
            emergency_serious_sumpatient-emergency_general_sumpatient
        return emergency_sumlist

    def emergency_general_get_patientNO(general_queue, current_time):
        # 用户挂号成功，成功进入排队队列
        global emergency_general_patientnumber, patientinf
        emergency_general_i = 0
        while emergency_general_i < emergency_general_queuenumber[current_time]:
            emergency_general_patientnumber = emergency_general_patientnumber+1
            emergency_general_i = emergency_general_i+1
            ArrayQueue.enqueue(general_queue, emergency_general_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """insert into waittime(patientinfo,entertime) values(%d,%d)""" % (
                emergency_general_patientnumber, current_time)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()  # 事务代码
            except Exception as e:
                print("添加失败", e)
                db.rollback()  # 发生错误 回滚事务
            db.close()  # 最后关闭连接

    def emergency_serious_get_patientNO(serious_queue, current_time):
        # 用户挂号成功，成功进入排队队列
        global emergency_serious_patientnumber, patientinf
        emergency_serious_i = 0
        while emergency_serious_i < emergency_serious_queuenumber[current_time]:
            emergency_serious_patientnumber = emergency_serious_patientnumber+1
            emergency_serious_i = emergency_serious_i+1
            ArrayQueue.enqueue(serious_queue, emergency_serious_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """insert into waittime(patientinfo,entertime) values(%d,%d)""" % (
                emergency_serious_patientnumber, current_time)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()  # 事务代码
            except Exception as e:
                print("添加失败", e)
                db.rollback()  # 发生错误 回滚事务
            db.close()  # 最后关闭连接

    def emergency_critical_get_patientNO(critical_queue, current_time):
        # 用户挂号成功，成功进入排队队列
        global emergency_critical_patientnumber, patientinf
        emergency_critical_i = 0
        while emergency_critical_i < emergency_critical_queuenumber[current_time]:
            emergency_critical_patientnumber = emergency_critical_patientnumber+1
            emergency_critical_i = emergency_critical_i+1
            ArrayQueue.enqueue(
                critical_queue, emergency_critical_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """insert into waittime(patientinfo,entertime) values(%d,%d)""" % (
                emergency_critical_patientnumber, current_time)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()  # 事务代码
            except Exception as e:
                print("添加失败", e)
                db.rollback()  # 发生错误 回滚事务
            db.close()  # 最后关闭连接

    def emergency_dequeueandpush(self):
        # 模拟急诊排队队列出队并入栈过程
        while ArrayStack.__len__(emergency_stack) < emergency_group and ArrayQueue.__len__(self) > 0:
            emergency_exit = ArrayQueue.dequeue(self)
            ArrayStack.push(emergency_stack, emergency_exit)

    def emergency_stackpop(self):
        global emergency_group
        stackpopsize = ArrayStack.__len__(self)
        for stackpopnumber in range(stackpopsize):
            emergency_exitpatientinf = ArrayStack.pop(self)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """update waittime set exittime=%d where patientinfo=%d""" % (
                current_time, emergency_exitpatientinf)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()  # 事务代码
            except Exception as e:
                print("添加失败", e)
                db.rollback()  # 发生错误 回滚事务
            db.close()  # 最后关闭连接


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
    global sum_time, current_time, emergency_general_loc, emergency_general_scale, emergency_serious_loc, emergency_serious_scale, emergency_critical_loc, emergency_critical_scale, emergency_group
    global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
    global emergency_general_patientnumber, emergency_serious_patientnumber, emergency_critical_patientnumber
    global emergency_stack
    global emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient

    # 输入
    sum_time = int(input("请输入总时间（单位：分钟）："))
    normal_loc = float(input("请输入每分钟门诊病人到达人数正态分布的均值："))
    normal_scale = float(input("请输入每分钟门诊病人到达人数正态分布的标准差："))
    normal_group = int(input("请输入服务门诊病人的窗口总数："))
    emergency_general_loc = float(input("请输入每分钟急诊一般病人到达人数正态分布的均值："))
    emergency_general_scale = float(input("请输入每分钟急诊一般病人到达人数正态分布的标准差："))
    emergency_serious_loc = float(input("请输入每分钟急诊严重病人到达人数正态分布的均值："))
    emergency_serious_scale = float(input("请输入每分钟急诊严重病人到达人数正态分布的标准差："))
    emergency_critical_loc = float(input("请输入每分钟急诊危重病人到达人数正态分布的均值："))
    emergency_critical_scale = float(input("请输入每分钟急诊危重病人到达人数正态分布的标准差："))
    emergency_group = int(input("请输入服务急诊病人的窗口总数："))

    # 处理门诊数据
    normal_queuenumber = list()
    normal_sumlist = normal.sum_normalpatient(sum_time)
    print("门诊要服务的总用户人数为%d" % (normal_sumlist))
    emergency_general_queuenumber = list()
    emergency_serious_queuenumber = list()
    emergency_critical_queuenumber = list()
    emergency_sumlist = emergency.sum_emergencypatient(sum_time)
    print("急诊要服务的总用户人数为%d，一般患者人数为%d人，严重患者人数为%d人，危重患者人数为%d人" % (emergency_sumlist,
          emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient))
    normal_queue = ArrayQueue()
    current_time = 0
    dt_time = datetime.datetime.now()
    nowtime = int(gettime.to_integer(dt_time))
    normal_patientnumber = nowtime*100000+10000
    general_queue = ArrayQueue()
    serious_queue = ArrayQueue()
    critical_queue = ArrayQueue()
    current_time = 0
    emergency_general_patientnumber = nowtime*100000+20000
    emergency_serious_patientnumber = nowtime*100000+23000
    emergency_critical_patientnumber = nowtime*100000+26000

    while current_time < sum_time:
        normal.normal_get_patientNO(normal_queue, current_time)
        normal.normal_dequeue(normal_queue)
        emergency.emergency_general_get_patientNO(general_queue, current_time)
        emergency.emergency_serious_get_patientNO(serious_queue, current_time)
        emergency.emergency_critical_get_patientNO(
            critical_queue, current_time)
        emergency_stack = ArrayStack()
        emergency.emergency_dequeueandpush(critical_queue)
        emergency.emergency_dequeueandpush(serious_queue)
        emergency.emergency_dequeueandpush(general_queue)
        emergency.emergency_stackpop(emergency_stack)
        current_time = current_time+1

    print()
    print("经过%d分钟，门诊病人完成诊疗人数为%d人" %
          (sum_time, int(normal_sumlist)-int(ArrayQueue.__len__(normal_queue))))
    print("门诊病人剩下人数为%d人" % (ArrayQueue.__len__(normal_queue)))
    print()
    print("经过%d分钟，急诊病人完成一般患者人数%d人，完成严重患者人数%d人，完成危重患者人数%d人" %
          (sum_time, int(emergency_sumlist)-int(ArrayQueue.__len__(general_queue)), int(emergency_sumlist)-int(ArrayQueue.__len__(serious_queue)), int(emergency_sumlist)-int(ArrayQueue.__len__(critical_queue))))
    print("急诊病人剩下一般患者人数%d人，剩下严重患者人数%d人，剩下危重患者人数%d人" % (ArrayQueue.__len__(
        general_queue), ArrayQueue.__len__(serious_queue), ArrayQueue.__len__(critical_queue)))
    average_waittime = alluse.averagewaittime()
    print("所有病人的平均等待时间为%f分钟" % (average_waittime))
