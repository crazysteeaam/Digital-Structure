class ADT:
    blist = []
    alist = list()
    # 创建函数

    def initlist(alist):
        n = int(input("请输入元素总数："))
        if(n > 25 or n < 1):
            print("Error!")
            return
        for i in range(n):
            alist[i] = input("请输入元素：.......\n")
        return

    # 打印函数
    def Print(alist):
        print(alist)

    # 查找函数
    def Search(alist, n, m):
        if (m > n or m < 1):
            print("Error!\n")
            return
        else:
            print("元素%d在第%d个位置" % (alist[m-1], m))
            return

    # 插入函数
    def Insert(alist, n, m, elem):
        if (m < 1 or m > n):
            print("Error!\n")
            return
        for j in range(m-1):
            alist[j+1] = alist[j]
        alist[m-1] = elem
        n = n+1
        print("插入后的新列表：")
        ADT.Print(alist)
        return

    # 删除函数
    def Delete(alist, n, m):
        q = m-1
        if (m < 1 or m > n):
            print("Error!\n")
            return
        while q <= n:
            alist[q] = alist[q+1]
            q = q+1
        print("删除后的新列表：")
        ADT.Print(alist)
        return

    # 目录函数
    def menu():
        alist = list()
        print("***************** MENU *****************")
        print("创建新列表：.................press 1\n\n")
        print("打印全列表：.................press 2\n\n")
        print("查询列表：...................press 3\n\n")
        print("在i处插入元素：..............press 4\n\n")
        print("删除元素：...................press 5\n\n")
        print("结束程序：...................press 0\n\n")
        print("***************** END ******************")
        j = int(input("请在0~6中选择数字输入：................."))
        if (j < 0 or j > 7):
            print("Error!请重新选择数字.......")
            return
        print("\n\t 你选择的数字是%d\n" % j)
        print("\n\t 按任意按键继续......")
        if j == 1:
            ADT.initlist()
            return

        elif j == 2:  # 打印该线性表
            print("原始列表是：")
            ADT.Print(alist, n)
            print("任意按键继续......")
            return
        elif j == 3:  # 查找第i个元素并返回其值
            a = int(input("请输入你想要查找元素的位置："))
            ADT.Search(alist, n, a)
            print("任意按键继续......")
            return

        elif j == 4:  # 在第i个元素前插入一已知元素
            k = int(input("请输入要插入元素的位置："))
            eleminsert = int(input("请输入要插入的元素："))
            ADT.Insert(alist, n, k, eleminsert)
            print("任意按键继续......")
            return

        elif j == 5:  # 在线性表中删除第i个元素
            l = int(input("请输入要删除元素的位置："))
            n = n+1
            ADT.Delete(alist, n, 1)
            n-n-1
            print("任意按键继续......")
            return

        elif j == 0:
            print("任意按键继续......")
            exit()


while True:
    menu()
