class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        s = s.strip()

        e = s.split()
        return " ".join(e[::-1])


if __name__ == '__main__':
    S = Solution()
    print(S.reverseWords("the sky is blue"))
