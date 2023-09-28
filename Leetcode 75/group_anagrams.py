from collections import defaultdict


class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        word_dict = defaultdict(list)  # or use normal dict with setting the word manually
        for word in strs:
            sorted_word = "".join(sorted(word))

            word_dict[sorted_word].append(word)

        return list(word_dict.values())


if __name__ == '__main__':
    words = ['eat', 'bat', 'tab', 'tea', 'sea', 'cat', 'sat']

    S = Solution()
    print(S.groupAnagrams(words))
