class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        sdict = {}
        tdict = {}
        if len(s) != len(t):
            return False
        for letter in sorted(s):
            if letter not in sdict:
                sdict[letter] = 1
            else:
                sdict[letter] += 1

        for letter in sorted(t):
            if letter not in tdict:
                tdict[letter] = 1
            else:
                tdict[letter] += 1

        return sdict == tdict
    # or use .get("val",0)-1 or + 1 and check for values ==0


if __name__ == '__main__':
    S = Solution()
    print(S.isAnagram("rat", "ar"))
