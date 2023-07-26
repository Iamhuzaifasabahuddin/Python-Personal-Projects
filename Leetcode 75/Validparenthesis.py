class Solution(object):
    def isValid(self, s):
        valid = {')': '(', ']': '[', '}': '{'}
        res = []
        for value in s:
            if value not in valid:
                res.append(value)
            elif res and res[-1] == valid[value]:
                res.pop()
            else:
                return False

        return res == []  # or use not res


if __name__ == '__main__':
    S = Solution()
    print(S.isValid(")"))
