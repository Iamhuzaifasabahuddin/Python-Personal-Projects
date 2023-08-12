class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root) -> int:

        head = root
        if head:
            return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
        else:
            return 0
