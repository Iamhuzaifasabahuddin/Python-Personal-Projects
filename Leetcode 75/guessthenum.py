class Solution:
    def guessNumber(self, n: int) -> int:
        l, r = 1, n

        while l <= r:
            mid = l + (r - l) // 2
            res = guess(mid)

            if res == 0:
                return mid
            if res == -1:
                r = mid - 1
            else:
                l = mid + 1
        return -1
