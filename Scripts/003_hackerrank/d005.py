#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Day 5: Loops

Source : https://www.hackerrank.com/challenges/30-loops/problem
"""
n = int(input())
for i in range(1,11):
    print("{} x {} = {}".format(n, i, n*i))
