class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        # Remove non-alphanumeric characters and convert to lowercase
        cleaned_s = "".join(char.lower() for char in s if char.isalnum())
        # Check if the cleaned string is a palindrome
        return cleaned_s == cleaned_s[::-1]


if __name__ == '__main__':
    S = Solution()
    print(S.isPalindrome("A man, a plan, a canal: Panama"))
