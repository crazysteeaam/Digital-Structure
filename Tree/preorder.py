
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children


class Solution:
    #递归法
    def preorder_recursive(self, root: 'Node') -> List[int]:
        value=list()
        def pre_order(root):
            if root:
                value.append(root.val)
                for node in root.children:
                    pre_order(node)
        pre_order(root)
        return value

    #迭代法
    def preorder_iterative(self, root: 'Node') -> List[int]:
        value, s = [], []
        if root:
            s.append(root)
        while s:
            cur = s.pop()
            value.append(cur.val)
            s.extend(cur.children[::-1])
        return value