class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def leafSimilar(self, root1, root2):
        def get_leaf_sequence(root):
            if not root:
                return []
            if not root.left and not root.right:
                return [root.val]
            return get_leaf_sequence(root.left) + get_leaf_sequence(root.right)
        leaf_sequence1 = get_leaf_sequence(root1)
        leaf_sequence2 = get_leaf_sequence(root2)

        return leaf_sequence1 == leaf_sequence2


# Create the tree structures
tree1 = TreeNode(3)
tree1.left = TreeNode(9)
tree1.right = TreeNode(20)
tree1.right.left = TreeNode(15)
tree1.right.right = TreeNode(7)

tree2 = TreeNode(3)
tree2.left = TreeNode(20)
tree2.right = TreeNode(9)
tree2.left.left = TreeNode(7)
tree2.left.right = TreeNode(15)

# Create an instance of the Solution class
solution = Solution()

# Determine if the leaf sequences are similar
result = solution.leafSimilar(tree1, tree2)
print(result)
