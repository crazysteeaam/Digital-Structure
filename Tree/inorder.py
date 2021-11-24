# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    #递归法
    def inorderTraversal_recursive(self, root: TreeNode) -> List[int]:
        value=list()
        def inorder_travel(root):
            if root:
                inorder_travel(root.left)
                value.append(root.val)
                inorder_travel(root.right)
        inorder_travel(root)
        return value

    #迭代法
    def inorderTraversal_iterative(self, root: TreeNode) -> List[int]:
        value,s=[],[]
        cur = root
        while s or cur:
            if cur:
                s.append(cur)
                cur=cur.left
            else:
                cur=s.pop()
                value.append(cur.val)
                cur=cur.right
        return value