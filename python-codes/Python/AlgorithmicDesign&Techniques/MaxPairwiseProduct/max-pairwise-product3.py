#!/usr/bin/env python3

n = int(input())
a = [int(x) for x in input().split()]

if a[0] >= a[1]:
    max1_idx = 0
    max2_idx = 1
else:
    max1_idx = 1
    max2_idx = 0

max1 = a[max1_idx]
max2 = a[max2_idx]

for i in range(2,n):
    if a[i] > max1:
        max2_idx = max1_idx
        max2 = max1
        max1_idx = i
        max1 = a[max1_idx]
    elif a[i] > max2:
        max2_idx = i
        max2 = a[max2_idx]

print(max1 * max2)
