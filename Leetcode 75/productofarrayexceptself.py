class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        alist = [1] * len(nums)
        pre = 1
        for i in range(len(nums)):
            alist[i] = pre
            pre *= nums[i]
        post = 1
        for i in range(len(nums) - 1, -1, -1):
            alist[i] *= post
            post *= nums[i]
        return alist
