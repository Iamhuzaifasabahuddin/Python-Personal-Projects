class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        nums.sort()

        for i, value in enumerate(nums):
            if i > 0 and value == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                threesum = value + nums[left] + nums[right] 
                if threesum > 0:
                    right -= 1
                if threesum < 0:
                    left += 1
                else:
                    result.append([value, nums[left], nums[right]])
                    left += 1
                    while left < right and left == nums[i - 1]:
                        left = left + 1
                   # reference why do we use a loop is to move forward as 
                   # if to decrement it the previous conditions do that for you.
                   # We could also use 3 for loop method
                   # for i in range(len(nums)-2): because last two wont be checked.
                   #     for j in rane(i,len(nums)-1): last wont be checked.
                   #         for k in range(j, len(nums)):

        return result
