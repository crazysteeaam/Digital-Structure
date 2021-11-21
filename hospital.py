# 链表ADT
import util
from util.Empty import Empty
from util.Outbound import Outboun


class Node:
    def init(self, value=None, next=None):
        self.value = value
        self.next = next


class SingleLinkedList:
    def init(self):
        self.head = Node()
        self.tail = None
        self.length = 0

    def peek(self):
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        return self.head.next

    def get_first(self):
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        return self.head.next

    def get_last(self):
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        node = self.head
        while node.next != None:
            node = node.next
        return node

    def get(self, index):
        if (index < 0 or index >= self.length):
            raise Outbound('index is out of bound')
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        node = self.head.next
        for i in range(index):
            node = node.next
        return node

    def add_first(self, value):
        node = Node(value, None)
        node.next = self.head.next
        self.head.next = node
        self.length += 1

    def add_last(self, value):
        new_node = Node(value)
        node = self.head
        while node.next != None:
            node = node.next
        node.next = new_node
        self.length += 1

    def add(self, index, value):
        if (index < 0 or index > self.length):
            raise Outbound('index is out of bound')
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        new_node = Node(value)
        node = self.head
        for i in range(index):
            node = node.next
        new_node.next = node.next
        node.next = new_node
        self.length += 1

    def remove_first(self):
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        value = self.head.next
        self.head.next = self.head.next.next
        self.length -= 1
        return value

    def remove_last(self):
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        node = self.head.next
        prev = self.head
        while node.next != None:
            prev = node
            node = node.next
        prev.next = None
        return node.value

    def remove(self, index):
        if (index < 0 or index >= self.length):
            raise Outbound('index is out of bound')
        if not self.head.next:
            raise Empty('SingleLinkedList is empty')
        node = self.head
        for i in range(index):
            node = node.next
        result = node.next
        node.next = node.next.next
        self.length += 1
        return result


# 栈ADT
class ArrayStack(object):
    def init(self):
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

# 队列ADT


class ArrayQueue:
    DEFAULT_CAPACITY = 2

    def init(self):
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
            self._resize(2 * len(self._data))
        pos = (self._front + self._size) % len(self._data)
        self._data[pos] = e
        self._size += 1
