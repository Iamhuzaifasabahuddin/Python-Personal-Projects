class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        comp = prices[0]
        max = 0
        for i, value in enumerate(prices):
            if value < comp:
                comp = value
            diff = value - comp
            if diff > max:
                max = diff
        return max
