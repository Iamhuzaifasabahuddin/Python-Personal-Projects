# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return None  # Base case: empty tree or value not found

        if root.val == val:
            return root  # Value found at the current node

        if val < root.val:
            return self.searchBST(root.left, val)  # Search in the left subtree
        else:
            return self.searchBST(root.right, val)  # Search in the right subtree
