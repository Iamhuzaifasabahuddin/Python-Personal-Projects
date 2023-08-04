class Solution(object):
    def compress(self, chars):
        """
        :type chars: List[str]
        :rtype: int
        """
        compressed_str = ""
        count = 1

        for i in range(len(chars) - 1):
            if chars[i] == chars[i + 1]:
                count += 1
            else:
                compressed_str += chars[i] + (str(count) if count > 1 else "")
                count = 1

        compressed_str += chars[-1] + (str(count) if count > 1 else "")

        if len(compressed_str) < len(chars):
            chars = list(compressed_str)
            return len(compressed_str), chars


if __name__ == '__main__':
    S = Solution()
    print(S.compress(["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]))
