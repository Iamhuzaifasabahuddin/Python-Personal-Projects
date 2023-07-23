class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        res = 0
        # for i in range(len(height)-1):
        #     for j in range(i+1, len(height)):
        #         print(i,j)
        #         area = (j - i) * min(height[j], height[i])
        #         print(area)
        #         res = max(area, res)
        # return res

        l, r = 0, len(height) - 1
        while l <= r:
            area = (r - l) * min(height[l], height[r])
            res = max(area, res)
            if height[l] < height[r]:
                l += 1
            # if height[r] < height[l]: # can incremenet or decremenet same thing hence else
            else:
                r -= 1
        return res


if __name__ == '__main__':
    S = Solution()
    print(S.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))
