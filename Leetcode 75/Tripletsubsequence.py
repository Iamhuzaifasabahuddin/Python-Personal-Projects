class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        if len(nums) < 3:
            return False

        first_min = float('inf')  # Initialize with positive infinity
        second_min = float('inf')  # Initialize with positive infinity

        for num in nums:

            if num <= first_min:
                first_min = num
            elif num <= second_min:
                second_min = num
            else:
                return True
        return False


# class Solution:
#     def increasingTriplet(self, nums: list[int]) -> bool:
#         n = len(nums)
#         maxRight = [0] * n  # maxRight[i] is the maximum element among nums[i+1...n-1]
#         maxRight[-1] = nums[-1]
#         for i in range(n - 2, -1, -1):
#             maxRight[i] = max(maxRight[i + 1], nums[i + 1])
#         minLeft = nums[0]
#         for i in range(1, n - 1):
#             if minLeft < nums[i] < maxRight[i]:
#                 return True
#             minLeft = min(minLeft, nums[i])
#         return False

if __name__ == '__main__':
    S = Solution()
    print(S.increasingTriplet([20, 100, 10, 12, 5, 13]
                              ))
