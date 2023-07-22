class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        currmin, currmax = 1, 1
        res = max(nums)

        for n in nums:
            if n == 0:
                currmin, currmax = 1, 1
                continue
            temp = n * currmax
            currmax = max(n * currmax, n * currmin, n)
            currmin = min(temp, n * currmin, n)

            res = max(res, currmax, currmin)
        return res


if __name__ == '__main__':
    S = Solution()
    print(S.maxProduct([2, 3, -2, 4]))
