'''
    Program to check if all the numbers is an array are of the same order.

    IP: [1,2,3,4,5] OP: True
    IP: [100, 10, 11, 12, 13]

'''

def is_constant_order(nums, tolerance):
    order = dict()
    for num in nums:
        if num < 0:
            return False
        if num == 0:
            order[num] = 0
        if num == 1:
            order[num] = 0
        if num < 1:
            e = 0
            while(num < 1):
                num *= 10
                e -= 1
            order[num] = e
        if num > 1:
            e = 0
            while(num > 1):
                e += 1
                num /= 10
            order[num] = e

    num = nums[0]
    for i in range(1, len(nums)):
        if abs(nums[i] - num) > tolerance:
            return False
    return True

