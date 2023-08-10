class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        len1, len2 = len(str1), len(str2)

        # Check if the combined strings are equal in both orders
        if str1 + str2 != str2 + str1:
            return ""

        # Find the greatest common divisor of lengths
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        gcd_length = gcd(len1, len2)
        return str1[:gcd_length]


if __name__ == '__main__':
    S = Solution()
    print(S.gcdOfStrings("ABABAB", "ABAB"))
