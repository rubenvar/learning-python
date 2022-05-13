# prove that binary search is faster than nive search

# naive seach: scan entire list and ask if it's equal to the target
# if yes, return index
# if no, return -1
import random
import time


def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1


# binary search uses divede and conquer:
# leverage the fact that the list is SORTED
def binary_search(l, target, low=None, high=None):
    # # first started like this:
    # midpoint = (len(l)) // 2

    # if l[midpoint] == target:
    #     return midpoint
    # elif target < l[midpoint]:
    #     return binary_search(¿¿??, target)
    # else:
    #     # target > l[midpoint]
    #     return binary_search(¿¿??, target)

    # # but what to pass to the recursing ones?? like this:
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    # should never happen, except target is not in list at all
    if high < low:
        return -1

    midpoint = (low + high) // 2

    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        # target > l[midpoint]
        return binary_search(l, target, midpoint + 1, high)


if __name__ == '__main__':
    # # simple
    # l = [1, 3, 5, 10, 12]
    # target = 10
    # print(naive_search(l, target))
    # print(binary_search(l, target))

    # create a sorted list of 10000 random integers
    length = 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))

    start = time.time()
    # search for every value in sorted_list (run search 10000 times)
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Naive search time: ", end - start, "seconds")

    start = time.time()
    # again with binary_search
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary search time:", end - start, "seconds")
