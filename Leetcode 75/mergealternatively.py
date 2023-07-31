class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """
        res = ''

        len1, len2 = len(word1), len(word2)

        min_len = min(len1, len2)

        for i in range(min_len):
            res += word1[i] + word2[i]

        res += word1[min_len:] + word2[min_len:]

        return res


if __name__ == '__main__':
    S = Solution()
    print(S.mergeAlternately("ab", "pqr"))
