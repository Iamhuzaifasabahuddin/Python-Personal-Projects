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


if __name__ == '__main__':
    S = Solution()
    print(S.increasingTriplet([20, 100, 10, 12, 5, 13]
                              ))
