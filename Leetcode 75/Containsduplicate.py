class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        alist = []
        for items in nums:
            if items not in alist:
                alist.append(items)
            else:
                return True
        return False
