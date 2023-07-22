class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        nums.sort()

        for i, value in enumerate(nums):
            if i > 0 and value == nums[i + 1]:
                continue
            left, right = 0, len(nums) - 1
            while left < right:
                threesum = nums[left] + nums[right] + value
                if threesum > 0:
                    right -= 1
                if threesum < 0:
                    left += 1
                else:
                    result.append([value, nums[left], nums[right]])
                    left += 1
                    while left < right and left == nums[i - 1]:
                        left = left + 1
        return result
