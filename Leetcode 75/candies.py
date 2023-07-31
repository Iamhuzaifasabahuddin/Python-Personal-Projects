class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        """
        :type candies: List[int]
        :type extraCandies: int
        :rtype: List[bool]
        """
        comp = max(candies)
        res = []

        for candy in candies:
            calc = candy + extraCandies
            if calc >= comp:
                res.append(True)
            else:
                res.append(False)
        return res


if __name__ == '__main__':
    S = Solution()
    print(S.kidsWithCandies([2, 3, 5, 1, 3], 3))
