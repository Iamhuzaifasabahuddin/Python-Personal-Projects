class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        vowels = set("aeiouAEIOU")
        s = list(s)
        swap1, swap2 = 0, len(s) - 1

        while swap1 < swap2:
            while s[swap1] not in vowels and swap1 < swap2:
                swap1 += 1
            while s[swap2] not in vowels and swap1 < swap2:
                swap2 -= 1

            # Swap the vowels
            s[swap1], s[swap2] = s[swap2], s[swap1]

            swap1 += 1
            swap2 -= 1

        # Convert the list back to a string
        return "".join(s)


if __name__ == '__main__':
    S = Solution()
    print(S.reverseVowels("leetcode"))
