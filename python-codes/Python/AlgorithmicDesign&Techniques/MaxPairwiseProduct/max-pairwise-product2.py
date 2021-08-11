#!/usr/bin/env python3

n = int(input())
a = [int(x) for x in input().split()]

max1_idx = 0
max1 = a[max1_idx]
for i in range(1,n):
    if a[i] > max1:
        max1_idx = i
        max1 = a[i]

max2_idx = 1 if max1_idx == 0 else 0
max2 = a[max2_idx]
for i in range(max2_idx+1,n):
    if i != max1_idx:
        if a[i] > max2:
            max2_idx = i
            max2 = a[i]

print(max1 * max2)
