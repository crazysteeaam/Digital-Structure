class SingleNode(object):
    """"单链表的结点""""

    def __init__(self, item):
        # _item存放数据元素
        self.item = item
        # next是下个节点的标识
        self.next = None


class SingleLinkList(object):
    """单链表"""

    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        """链表是否为空"""
        return self.__head == None

    def length(self):
        """链表长度"""
        # cur游标，用来移动遍历节点
        cur = self.__head
        # count记录数量
        count = 0
        while cur != None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """遍历整个链表"""
        # cur游标，用来移动遍历节点
        cur = self.__head
        while cur != None:
            print(cur.item, end=" ")
            cur = cur.next
        print("")

    def add(self, item):
        """链表头部增加元素，头插法"""
        node = SingleNode(item)
        node.next = self.__head
        self.__head = node

    def append(self, item):
        """链表尾部增加元素，尾插法"""
        node = SingleNode(item)
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next != None:
                cur = cur.next
            cur.next = node

    def insert(self, pos, item):
        """
        指定位置添加元素
        :pos 从0开始索引
        """
        if pos < 0:
            self.add(item)
        elif pos > (self.length()-1):
            self.append(item)
        else:
            node = SingleNode(item)
            pre = self.__head
            count = 0
            while count < pos-1:
                pre = pre.next
                count += 1
            # 当循环退出后，pre指向pos-1位置
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        """删除节点"""
        if self.search(item):
            cur = self.__head
            pre = None
            while cur != None:
                if cur.item == item:
                    # 先判断此结点是非是头节点
                    # 头节点
                    if cur == self.__head:
                        self.head = cur.next
                    else:
                        pre.next = cur.next
                    break
                else:
                    pre = cur
                    cur = cur.next
        else:
            print("元素不在列表中")

    def removepos(self, pos):
        if pos >= 1 and pos <= li.length()-1:
            cur = self.__head
            pre = None
            count = 0
            while count < pos-1:
                pre = pre.next
                count += 1
            cur = pre.next
            cur = cur.next
            pre.next = cur
        elif pos == 0:
            cur = self.__head
            self.__head = cur.next
        else:
            print("元素不在列表中")

    def search(self, item):
        """查找节点是否存在"""
        cur = self.__head
        while cur != None:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        return False

    def removerpos(self, rpos):
        """删除倒数第n个结点"""
        pos = self.length()-rpos
        self.removepos(pos)
