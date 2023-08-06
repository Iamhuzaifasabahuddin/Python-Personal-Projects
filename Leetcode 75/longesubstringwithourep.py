class Solution(object):
    def lengthOfLongestSubstring(self, s):
        res = 0
        r = 0
        setter = set()
        for i in range(len(s)):
            while s[i] in setter:
                setter.remove(s[r])
                r += 1
            setter.add(s[i])
            res = max(res, i - r + 1)
        return res


if __name__ == '__main__':
    S = Solution()
    print(S.lengthOfLongestSubstring("abcabcbb"))
