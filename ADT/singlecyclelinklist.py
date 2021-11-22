class SingleNode(object):
    """"结点""""
    def __init__(self,item):
        #_item存放数据元素
        self.item=item
        #next是下个节点的标识
        self.next=None

class SingleLinkList(object):
    """单向循环链表"""

    def __init__(self, node=None):
        self.__head = node
        if node:
            node.next=node

    def is_empty(self):
        """链表是否为空"""
        return self.__head == None

    def length(self):
        """链表长度"""
        if self.is_empty():
            return 0
        # cur游标，用来移动遍历节点
        cur = self.__head
        # count记录数量
        count = 1
        while cur.next != self.__head:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """遍历整个链表"""
        # cur游标，用来移动遍历节点
        if self.is_empty():
            return 0
        cur = self.__head
        while cur.next != self._head:
            print(cur.item, end=" ")
            cur = cur.next
        """退出循环，cur指向尾结点，打印尾结点坐标"""
        print(cur.item)

    def add(self, item):
        """链表头部增加元素，头插法"""
        node = SingleNode(item)
        if self.is_empty():
            self.__head=node
            node.next=node
        else:
            cur=self.__head
            while cur.next != self.__head:
                cur=cur.next
            cur.next=node
            node.next = self.__head
            self.__head = node

    def append(self, item):
        """链表尾部增加元素，尾插法"""
        node = SingleNode(item)
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            cur.next = node
            node.next=self.__head

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
            while cur.next != self.__head:
                if cur.item == item:
                    # 先判断此结点是非是头节点
                    if cur == self.__head:
                        # 头节点
                        # 找尾结点
                        rear=self.__head
                        while rear.next != self.__head:
                            rear=rear.next
                        rear.next=cur.next
                        self.__head = cur.next


                    else:
                        #中间结点
                        pre.next = cur.next
                    break
                else:
                    pre = cur
                    cur = cur.next
            #尾结点
            if cur.item==item:

        else:
            print("元素不在列表中")     

    def search(self, item):
        """查找节点是否存在"""
        if self.is_empty():
            return False
        cur = self.__head
        while cur.next != self.__head:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        if cur.item == item:
            return True
        return False

    def removerpos(self,rpos):
        """删除倒数第n个结点"""
        pos=self.length()-rpos
        self.removepos(pos)