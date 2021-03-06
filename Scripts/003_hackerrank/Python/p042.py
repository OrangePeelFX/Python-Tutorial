#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Problem 042

Array Mathematics

Source : https://www.hackerrank.com/challenges/np-array-mathematics/problem
"""
import numpy as np

n, m = map(int, input().split())
a = np.array([input().split() for _ in range(n)], int)
b = np.array([input().split() for _ in range(n)], int)
print(a+b, a-b, a*b, a//b, a%b, a**b, sep="\n"))
