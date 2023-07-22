class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        maxsub = nums[0]
        currnum = 0
        for n in nums:
            if currnum < 0:
                currnum = 0
            currnum = currnum + n
            maxsub = max(maxsub, currnum)
        return maxsub


if __name__ == '__main__':
    S = Solution()
    print(S.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
