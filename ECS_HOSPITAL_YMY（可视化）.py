from logging import critical
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import math
import numpy as np
import pandas as pd
import pymysql
import datetime
from sqlalchemy.sql.sqltypes import DateTime
import tkinter
from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt
from decimal import Decimal

plt.rcdefaults()
# Implement the default Matplotlib key bindings.

# 获取当前时间戳


class gettime():
    def to_integer(dt_time):
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day

# 用户界面设计


class hospitalGUI:
    # 标题
    global root, lbnormal_lamda1, lbnormal_lamda2, lbnormal_lamda3, lbnormal_lamda4, lbnormal_lamda5, lbnormal_lamda6, lbnormal_lamda7, lbnormal_lamda8
    root = Tk()
    root.title('医院仿真系统')
    root.geometry('600x600')
    lbtitle = Label(root, text='医院仿真系统',
                    fg='black',
                    font=('等线', 20),
                    width=20,
                    height=2,
                    relief=FLAT)
    lbtitle.pack()
    lbnormal_lamda1 = Label(root, text="")
    lbnormal_lamda1.pack()
    lbnormal_lamda2 = Label(root, text="")
    lbnormal_lamda2.pack()
    lbnormal_lamda3 = Label(root, text="")
    lbnormal_lamda3.pack()
    lbnormal_lamda4 = Label(root, text="")
    lbnormal_lamda4.pack()
    lbnormal_lamda5 = Label(root, text="")
    lbnormal_lamda5.pack()
    lbnormal_lamda6 = Label(root, text="")
    lbnormal_lamda6.pack()
    lbnormal_lamda7 = Label(root, text="")
    lbnormal_lamda7.pack()
    lbnormal_lamda8 = Label(root, text="")
    lbnormal_lamda8.pack()

    # 计算平均时间

    def part_averagewaittime():
        pass

    def get_value(v=0):
        # 滑块取值
        param = {}
        for key in scales.keys():
            param[key] = scales[key]['value'].get()
        paramVar.set(f"normal_lamda:{param['normal_lamda']}, normal_group:{param['normal_group']}, emergency_general_lamda:{param['emergency_general_lamda']}, emergency_serious_lamda:{param['emergency_serious_lamda']},emergency_critical_lamda:{param['emergency_critical_lamda']},emergency_group:{param['emergency_group']}")

        # 折线图
    def draw_chart(items):
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        y = [x[1] for x in items]
        x = [x[0] for x in items]
        a.plot(x, y)
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                                    fill=tkinter.BOTH,  # 填充方式
                                    expand=tkinter.YES)  # 随窗口大小调整而调整

    def emptydatabase():
        pass

    def run(value):
        global sum_time
        sum_time = value


# 队列ADT


class ArrayQueue(object):
    DEFAULT_CAPACITY = 2

    def __init__(self):
        # 队列初始化
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        # 求队列长度
        return self._size

    def is_empty(self):
        # 判断队列是否空
        return self._size == 0

    def first(self):
        # 输出队首
        if self.is_empty():
            raise ValueError('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        # 出队
        if self.is_empty():
            raise ValueError('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        # 入队
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
        # 打印队列
        for i in range(self._size):
            pos = (self._front + self._size - 1 - i) % len(self._data)
            #print(str(i), ": ", str(pos))
            print(self._data[pos], end=" ")
        print()

# 栈ADT


class ArrayStack(object):

    def __init__(self):
        # 栈初始化
        self._data = []

    def __len__(self):
        # 输出栈元素个数
        return len(self._data)

    def is_empty(self):
        # 判断栈是否空
        return len(self._data) == 0

    def push(self, e):
        # 入栈
        self._data.append(e)

    def top(self):
        # 输出栈顶元素
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data[-1]

    def pop(self):
        # 出栈
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data.pop()

    def printstack(self):
        # 打印栈
        for i in range(len(self._data)):
            print(self._data[i], end=' ')
        print()

# 通用函数


class alluse():
    def averagewaittime():
        global averagetime_results
        # 计算所有病人平均等待时间
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        sql = """UPDATE waittime SET exittime=%d WHERE exittime is NULL""" % (
            sum_time)  # 将在排队队列中未能诊疗的患者结束时间记录为停诊时间
        cursor.execute(sql)
        # 筛选今天的数据，计算等待时间=出队时间-入队时间，求平均值
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) AS waittimelength FROM waittime WHERE DATE(currentdate) = CURRENT_DATE"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        averagetime_results = cursor.fetchone()
        db.close()  # 最后关闭连接
        return averagetime_results

    def part_averagewaittime():
        global sum_time, part_percent_results
        # 将总时间平分为十段，输出每个阶段病人平均等待时间
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        part_length = sum_time/10
        part_1 = part_length
        part_2 = part_1+1+part_length
        part_3 = part_2+1+part_length
        part_4 = part_3+1+part_length
        # 筛选每段的数据，计算等待时间=出队时间-入队时间，求每段平均值
        sql = """SELECT ELT(INTERVAL (waittime.entertime, 0, %d, %d, %d, %d),'前1/5段','前2/5段','前3/5段','前4/5段','末1/5段') AS 时间段,\
	    AVG(waittime.exittime - waittime.entertime) AS 平均时间 \
        FROM waittime \
        WHERE DATE(currentdate) = CURRENT_DATE GROUP BY \
        elt(INTERVAL (waittime.entertime, 0, %d, %d, %d, %d),'前1/5段','前2/5段','前3/5段','前4/5段','末1/5段');""" % (part_1, part_2, part_3, part_4, part_1, part_2, part_3, part_4)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        part_percent_results_temp = cursor.fetchall()
        part_percent_results = list()
        for part_percent_i in range(len(part_percent_results_temp)):
            part_percent_results.append(
                part_percent_results_temp[part_percent_i])
        db.close()  # 最后关闭连接
        print(part_percent_results)
        hospitalGUI.draw_chart(part_percent_results)
        return part_percent_results

    def part_averagewaittime_drawchart():
        global part_percent_results
        alluse.part_averagewaittime()
        print(part_percent_results)
        hospitalGUI.draw_chart(part_percent_results)

    def customize_averagewaittime():
        # 用户自定义输入初始时间和最终时间，输出该阶段内到达病人平均等待时间
        customize_averagewaittime_starttime = int(input("请输入初始时间："))
        customize_averagewaittime_endtime = int(input("请输入结束时间："))
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) AS waittimelength \
        FROM waittime WHERE DATE(currentdate) = CURRENT_DATE AND entertime BETWEEN %d AND %d""" % (customize_averagewaittime_starttime, customize_averagewaittime_endtime)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        customize_averagewaittime_results = cursor.fetchone()
        db.close()  # 最后关闭连接
        print(customize_averagewaittime_results)
        return customize_averagewaittime_results

    def normalandemergency_averagewaittime():
        # 分门诊以及急诊各个程度进行平均时间统计
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) as av from waittime WHERE substr(patientinfo,9,1)='1'"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        normal_averagewaittime_results = cursor.fetchone()
        print("门诊患者平均等待时间为%d" % (normal_averagewaittime_results))
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) as av from waittime WHERE substr(patientinfo,9,1)='2'"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        emergency_averagewaittime_results = cursor.fetchone()
        print("急诊患者平均等待时间为%d" % (emergency_averagewaittime_results))
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) as av from waittime WHERE substr(patientinfo,9,2) in('20','21','22')"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        emergency_general_averagewaittime_results = cursor.fetchone()
        print("急诊一般患者平均等待时间为%d" % (emergency_general_averagewaittime_results))
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) as av from waittime WHERE substr(patientinfo,9,2) in('23','24','25')"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        emergency_serious_averagewaittime_results = cursor.fetchone()
        print("急诊严重患者平均等待时间为%d" % (emergency_serious_averagewaittime_results))
        sql = """SELECT AVG(waittime.exittime - waittime.entertime) as av from waittime WHERE substr(patientinfo,9,2) in('26','27','28',"29")"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        emergency_critical_averagewaittime_results = cursor.fetchone()
        print("急诊危重患者平均等待时间为%d" % (emergency_critical_averagewaittime_results))
        db.close()  # 最后关闭连接

    def emptydatabase():
        # 清空数据库，重置数据
        db = pymysql.connect(host="localhost", user="root",
                             password="Qqhh12345", database="ymyhospital", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        sql = """TRUNCATE TABLE waittime"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()  # 事务代码
        except Exception as e:
            print("添加失败", e)
            db.rollback()  # 发生错误 回滚事务
        db.close()  # 最后关闭连接

     # 门诊函数库


class normal():
    def normal_number(normal_lamda, sum_time):
        # 生成每分钟门诊病人到达人数
        """
        :param normal_loc: 单位时间内门诊病人到达的平均发生次数（泊松分布）
        :return:从泊松分布中产生的随机数
        """
        # 泊松分布中的随机数生成
        number = np.random.poisson(lam=normal_lamda, size=sum_time)
        # 返回值
        return number

    def sum_normalpatient(sum_time):
        # 计算门诊要服务的总用户人数
        global normal_queuenumber
        normal_queuenumber = normal.normal_number(
            normal_lamda, sum_time)
        normal_sumlist = 0
        for normalsumlist in range(len(normal_queuenumber)):
            # 遍历每分钟门诊挂号人数的序列求和
            normal_sumlist = normal_sumlist+normal_queuenumber[normalsumlist]
        return normal_sumlist

    def normal_get_patientNO(self, current_time):
        # 用户挂号成功，成功进入排队队列
        global normal_patientnumber, patientinf, normal_queuenumber
        normal_i = 0
        # 模拟每个用户的进队时间，连接数据库，将数据计入数据库
        while normal_i < normal_queuenumber[current_time]:
            normal_patientnumber = normal_patientnumber+1  # 每次循环，用户序号+1
            normal_i = normal_i+1
            ArrayQueue.enqueue(normal_queue, normal_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            sql = """insert into waittime(patientinfo,entertime) values(%d,%d)""" % (
                normal_patientnumber, current_time)  # 病人挂号成功，在数据库中插入病人的序号以及入队时间
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
        if normal_group <= ArrayQueue.__len__(self):  # 判断门诊窗口数量是否少于门诊队列中用户数量
            # 执行用户出队列的循环操作，连接数据库，将用户出队时间记入数据库
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
            # 当门诊窗口数量大于队列中用户数目时
            while ArrayQueue.__len__(self):
                # 直接出队
                ArrayQueue.dequeue(self)

# 急诊函数库


class emergency():
    def emergency_number(emergency_lamda, sum_time):
        # 生成每分钟急诊病人到达人数
        """
        :param emergency_lamda: 单位时间内急诊病人到达的平均发生次数（泊松分布）
        :return:从泊松分布中产生的随机数
        """
        # 泊松分布中的随机数生成
        number = np.random.poisson(lam=emergency_lamda, size=sum_time)
        # 返回值
        return number

    def sum_emergencypatient(sum_time):
        # 计算急诊要服务的总用户人数
        global emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient
        global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
        global emergency_general_lamda, emergency_serious_lamda, emergency_critical_lamda
        for enumsum_general in range(sum_time):
            # 计算急诊一般用户每分钟到的人数
            emergency_general_queuenumber = emergency.emergency_number(
                emergency_general_lamda, sum_time)
        for enumsum_serious in range(sum_time):
            # 计算急诊严重用户每分钟到的人数
            emergency_serious_queuenumber = emergency.emergency_number(
                emergency_serious_lamda, sum_time)
        for enumsum_critical in range(sum_time):
            # 计算急诊危重用户每分钟到的人数
            emergency_critical_queuenumber = emergency.emergency_number(
                emergency_critical_lamda, sum_time)
        emergency_sumlist = 0
        for emergencysumlist1 in range(len(emergency_general_queuenumber)):
            # 计算急诊一般用户总人数
            emergency_sumlist = emergency_sumlist + \
                emergency_general_queuenumber[emergencysumlist1]
        emergency_general_sumpatient = emergency_sumlist
        for emergencysumlist2 in range(len(emergency_serious_queuenumber)):
            # 计算急诊一般+严重用户总人数
            emergency_sumlist = emergency_sumlist + \
                emergency_serious_queuenumber[emergencysumlist2]
        emergency_serious_sumpatient = emergency_sumlist-emergency_general_sumpatient
        for emergencysumlist3 in range(len(emergency_critical_queuenumber)):
            # 计算急诊一般+严重+危重用户总人数
            emergency_sumlist = emergency_sumlist + \
                emergency_critical_queuenumber[emergencysumlist3]
        emergency_critical_sumpatient = emergency_sumlist - \
            emergency_serious_sumpatient-emergency_general_sumpatient
        return emergency_sumlist  # 返回急诊用户总人数

    def emergency_general_get_patientNO(general_queue, current_time):
        # 一般用户挂号成功，成功进入排队队列
        global emergency_general_patientnumber, patientinf
        global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
        emergency_general_i = 0
        # 模拟每个用户的进队时间，连接数据库，将数据计入数据库
        while emergency_general_i < emergency_general_queuenumber[current_time]:
            emergency_general_patientnumber = emergency_general_patientnumber+1  # 每循环一次，用户序号+1
            emergency_general_i = emergency_general_i+1
            ArrayQueue.enqueue(general_queue, emergency_general_patientnumber)
            db = pymysql.connect(host="localhost", user="root",
                                 password="Qqhh12345", database="ymyhospital", charset="utf8")
            cursor = db.cursor()
            # 病人挂号成功，在数据库中插入病人的序号以及入队时间
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
        # 严重用户挂号成功，成功进入排队队列
        global emergency_serious_patientnumber, patientinf
        global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
        emergency_serious_i = 0
        # 模拟每个用户的进队时间，连接数据库，将数据计入数据库
        while emergency_serious_i < emergency_serious_queuenumber[current_time]:
            emergency_serious_patientnumber = emergency_serious_patientnumber+1  # 每循环一次，用户序号+1
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
        # 危重用户挂号成功，成功进入排队队列
        global emergency_critical_patientnumber, patientinf
        global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
        emergency_critical_i = 0
        # 模拟每个用户的进队时间，连接数据库，将数据计入数据库
        while emergency_critical_i < emergency_critical_queuenumber[current_time]:
            emergency_critical_patientnumber = emergency_critical_patientnumber+1  # 每循环一次，用户序号+1
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
            # 当栈的空间小于急诊窗口数量且急诊队列非空时执行用户出队并入栈的循环操作
            emergency_exit = ArrayQueue.dequeue(self)
            ArrayStack.push(emergency_stack, emergency_exit)

    def emergency_stackpop(self):
        # 模拟急诊用户出栈过程
        global emergency_group
        stackpopsize = ArrayStack.__len__(self)
        for stackpopnumber in range(stackpopsize):
            # 栈非空即出栈
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


class mainexe():
    def main_button_click():
        global sum_time, normal_lamda, normal_scale, normal_sumlist, current_time, normal_patientnumber, normal_group, average_waittime  # 定义全局变量
        global normal_queuenumber, normal_queue  # 定义全局顺序表、队列
        global sum_time, current_time, emergency_general_lamda, emergency_general_scale, emergency_serious_lamda, emergency_serious_scale, emergency_critical_lamda, emergency_critical_scale, emergency_group
        global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
        global emergency_general_patientnumber, emergency_serious_patientnumber, emergency_critical_patientnumber
        global emergency_stack
        global emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient, emergency_sumlist
        global scales, paramVar, E1
        global general_queue, serious_queue, critical_queue
        global lbnormal_lamda1, lbnormal_lamda2, lbnormal_lamda3, lbnormal_lamda4, lbnormal_lamda5, lbnormal_lamda6, lbnormal_lamda7, lbnormal_lamda8
        global emergency_general_lamda, emergency_serious_lamda, emergency_critical_lamda
        global normal_lamda_scale, emergency_general_lamda_scale, emergency_serious_lamda_scale, emergency_critical_lamda_scale, normal_group_scale, emergency_group_scale
        global lbnormal_lamda, lbemergency_general_lamda, lbemergency_serious_lamda, lbemergency_critical_lamda, lbnormal_group, lbemergency_group

        hospitalGUI.run(E1.get())
        sum_time = int(sum_time)
        normal_lamda = normal_lamda_scale.get()
        emergency_general_lamda = emergency_general_lamda_scale.get()
        emergency_serious_lamda = emergency_serious_lamda_scale.get()
        emergency_critical_lamda = emergency_critical_lamda_scale.get()
        normal_group = normal_group_scale.get()
        emergency_group = 2
        print(sum_time)
        normal_queuenumber = list()
        normal_sumlist = normal.sum_normalpatient(sum_time)
        emergency_general_queuenumber = list()
        emergency_serious_queuenumber = list()
        emergency_critical_queuenumber = list()
        emergency_sumlist = emergency.sum_emergencypatient(sum_time)
        normal_queue = ArrayQueue()
        current_time = 0
        dt_time = datetime.datetime.now()
        nowtime = int(gettime.to_integer(dt_time))
        normal_patientnumber = nowtime*100000+10000  # 门诊用户序号格式
        general_queue = ArrayQueue()
        serious_queue = ArrayQueue()
        critical_queue = ArrayQueue()
        emergency_general_patientnumber = nowtime*100000+20000  # 急诊一般用户序号格式
        emergency_serious_patientnumber = nowtime*100000+23000  # 急诊严重用户序号格式
        emergency_critical_patientnumber = nowtime*100000+26000  # 急诊危重用户序号格式

        while current_time < sum_time:  # 直到用户的入队时间大于等于总服务开放时间，跳出循环
            normal.normal_get_patientNO(normal_queue, current_time)
            normal.normal_dequeue(normal_queue)
            emergency.emergency_general_get_patientNO(
                general_queue, current_time)
            emergency.emergency_serious_get_patientNO(
                serious_queue, current_time)
            emergency.emergency_critical_get_patientNO(
                critical_queue, current_time)
            emergency_stack = ArrayStack()
            emergency.emergency_dequeueandpush(critical_queue)
            emergency.emergency_dequeueandpush(serious_queue)
            emergency.emergency_dequeueandpush(general_queue)
            emergency.emergency_stackpop(emergency_stack)
            current_time = current_time+1
        average_waittime = alluse.averagewaittime()
        lbnormal_lamda1.config(text="门诊要服务的总用户人数为%d" % (normal_sumlist))
        lbnormal_lamda2.config(text="急诊要服务的总用户人数为%d，一般患者人数为%d人，严重患者人数为%d人，危重患者人数为%d人" % (emergency_sumlist,
                                                                                         emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient))
        lbnormal_lamda3.config(text="经过%d分钟，门诊病人完成诊疗人数为%d人" %
                               (sum_time, int(normal_sumlist)-int(ArrayQueue.__len__(normal_queue))))
        lbnormal_lamda4.config(text="经过%d分钟，门诊病人完成诊疗人数为%d人" %
                               (sum_time, int(normal_sumlist)-int(ArrayQueue.__len__(normal_queue))))
        lbnormal_lamda5.config(text="门诊病人剩下人数为%d人" %
                               (ArrayQueue.__len__(normal_queue)))
        lbnormal_lamda6.config(text="经过%d分钟，急诊病人完成一般患者人数%d人，完成严重患者人数%d人，完成危重患者人数%d人" %
                               (sum_time, int(emergency_sumlist)-int(ArrayQueue.__len__(general_queue)), int(emergency_sumlist)-int(ArrayQueue.__len__(serious_queue)), int(emergency_sumlist)-int(ArrayQueue.__len__(critical_queue))))
        lbnormal_lamda7.config(text="急诊病人剩下一般患者人数%d人，剩下严重患者人数%d人，剩下危重患者人数%d人" % (ArrayQueue.__len__(
            general_queue), ArrayQueue.__len__(serious_queue), ArrayQueue.__len__(critical_queue)))
        lbnormal_lamda8.config(text="所有病人的平均等待时间为%f分钟" % (average_waittime))


class main():
    db_info = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Qqhh12345',
        'database': 'ymyhospital',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**db_info)  # 连接数据库
    cursor = conn.cursor()

    # 定义全局变量
    global sum_time, normal_lamda, normal_scale, normal_sumlist, current_time, normal_patientnumber, normal_group, average_waittime  # 定义全局变量
    global normal_queuenumber, normal_queue  # 定义全局顺序表、队列
    global sum_time, current_time, emergency_general_lamda, emergency_general_scale, emergency_serious_lamda, emergency_serious_scale, emergency_critical_lamda, emergency_critical_scale, emergency_group
    global emergency_general_queuenumber, emergency_serious_queuenumber, emergency_critical_queuenumber
    global emergency_general_patientnumber, emergency_serious_patientnumber, emergency_critical_patientnumber
    global emergency_stack
    global emergency_general_sumpatient, emergency_serious_sumpatient, emergency_critical_sumpatient, emergency_sumlist
    global scales, paramVar, E1
    global general_queue, serious_queue, critical_queue
    global lbnormal_lamda1, lbnormal_lamda2, lbnormal_lamda3, lbnormal_lamda4, lbnormal_lamda5, lbnormal_lamda6, lbnormal_lamda7, lbnormal_lamda8
    global emergency_general_lamda, emergency_serious_lamda, emergency_critical_lamda
    global normal_lamda_scale, emergency_general_lamda_scale, emergency_serious_lamda_scale, emergency_critical_lamda_scale, normal_group_scale, emergency_group_scale
    global lbnormal_lamda, lbemergency_general_lamda, lbemergency_serious_lamda, lbemergency_critical_lamda, lbnormal_group, lbemergency_group

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    # 窗口参数设定
    root = Tk()
    root.title("医院仿真系统")
    root.geometry('450x600+400+400')    # 位置设置
    root.wm_resizable(False, False)   # 不允许修改长宽
    height = 500
    width = 500
    # 滑块参数设定
    normal_lamda_scale = Scale(
        root, length=200, label='每分钟门诊患者平均人数', from_=0, to=10, orient=HORIZONTAL)  # Scale组件
    normal_lamda_scale.grid(column=3, row=0)
    emergency_general_lamda_scale = Scale(
        root, length=200, label='每分钟急诊一般患者平均人数', from_=0, to=10, orient=HORIZONTAL)
    emergency_general_lamda_scale.grid(column=3, row=1)
    emergency_serious_lamda_scale = Scale(
        root, length=200, label='每分钟急诊严重患者平均人数', from_=0, to=10, orient=HORIZONTAL)
    emergency_serious_lamda_scale.grid(column=3, row=2)
    emergency_critical_lamda_scale = Scale(
        root, length=200, label='每分钟急诊危重患者平均人数', from_=0, to=10, orient=HORIZONTAL)
    emergency_critical_lamda_scale.grid(column=3, row=3)
    normal_group_scale = Scale(
        root, length=200, label='门诊窗口数', from_=0, to=10, orient=HORIZONTAL)
    normal_group_scale.grid(column=3, row=4)
    emergency_group_scale = Scale(
        root, length=200, label='急诊窗口数', from_=0, to=10, orient=HORIZONTAL)
    emergency_group_scale.grid(column=3, row=5)
    # 定义button
    btn1 = Button(root, text='清空现有数据', command=alluse.emptydatabase())
    btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
    btn1.grid(column=3, row=10)
    btn2 = Button(root, text='确定', command=lambda: mainexe.main_button_click())
    btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)
    btn2.grid(column=3, row=11)
    btn3 = Button(root, text='将总时长平分为五段，输出每个阶段病人平均等待时间',
                  command=lambda: alluse.part_averagewaittime_drawchart())
    btn3.place(relx=0.6, rely=0.4, relwidth=0.7, relheight=0.1)
    btn3.grid(column=3, row=12)

    # 输入框
    L1 = Label(root, text="服务总时长")
    L1.grid(column=3, row=8)
    E1 = Entry(root, bd=5)
    E1.grid(padx=20, column=3, row=9)
    # 反馈输出

    # 清空数据库按钮
    root.mainloop()
