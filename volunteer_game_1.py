#!/usr/bin/python3
__version__ = '0.0.1' # Time-stamp: <2020-03-01T02:36:42Z>
## Language: Japanese/UTF-8

"""A simple calculation of game theory for volunteers."""

##
## License:
##
##   Public Domain
##   (Since this small code is close to be mathematically trivial.)
##
## Author:
##
##   JRF
##   http://jrf.cocolog-nifty.com/software/
##   (The page is written in Japanese.)
##

import nashpy as nash
import numpy as np

print("\nQ1")
## ボランティアをすると、その労力に -1 の効用、達成感で +1 の効用、環境
## 改善で両者に +2 ずつの効用があるとする。両者がボランティアをすると両
## 者とも +1 の達成感を得るが、環境改善は +2 のまま、+4 とかにはならな
## いものとする。
##
## 仕事をすると、その労力に -1 の効用、達成感で +1 の効用、報酬 2 を得
## て効用が +2 とする。両者が仕事をした場合、報酬はそれぞれ 1 を得て効
## 用が +1 とする。
##
## 両者がボランティアをする場合、効用は、それぞれ 2。両者が仕事をすると、
## 効用は、それぞれ、1。片方が仕事、もう片方がボランティアの場合、仕事
## をしたほうが 4、ボランティアをしたほうが 2 になる。

A = np.array([[2, 4], [2, 1]])
B = np.array([[2, 2], [4, 1]])
G = nash.Game(A, B)

equilibria = G.support_enumeration()
for eq in equilibria:
    print(eq, np.sum(G[eq]))

print("\nQ2")
## ボランティアは全体として労力を -2 の効用分使う。一人でやれば -2、二
## 人でやれば -1。やれば達成感でそれぞれ +1 の効用がある。そして、環境
## 改善で両者に +2 ずつの効用があるとする。両者がボランティアをしても環
## 境改善は +2 のまま、+4 とかにはならないものとする。
##
## 仕事をすると、それぞれその労力に -1 の効用、達成感に +1 の効用。一人
## の場合は、報酬 3 を得て効用が +3 とする。両者が仕事をした場合、報酬
## それぞれ 2 を得て効用が +2 とする。
##
## 両者がボランティアをする場合、効用は、それぞれ 2。両者が仕事をすると、
## 効用は、それぞれ、2。片方が仕事、もう片方がボランティアの場合、仕事
## をしたほうが 5、ボランティアをしたほうが 1 になる。

A = np.array([[2, 1], [5, 2]])
B = np.array([[2, 5], [1, 2]])
G = nash.Game(A, B)

equilibria = G.support_enumeration()
for eq in equilibria:
    print(eq, np.sum(G[eq]))

print("\nQ3")
## Q2 に関して、報酬 2 をボランティアにまわす。
A = np.array([[2, 3], [3, 2]])
B = np.array([[2, 3], [3, 2]])
G = nash.Game(A, B)

equilibria = G.support_enumeration()
for eq in equilibria:
    print(eq, np.sum(G[eq]))

print("\nQ4")
## Q3 に関して、両者が仕事をする場合も 2/3 の税はとられるとする。
A = np.array([[2, 3], [3, 2 * 1 / 3]])
B = np.array([[2, 3], [3, 2 * 1 / 3]])
G = nash.Game(A, B)

equilibria = G.support_enumeration()
for eq in equilibria:
    print(eq, np.sum(G[eq]))

print("\nQ5")
## Q1 について、1/2 の税を導入した場合。

A = np.array([[2, 3], [3, 1/2]])
B = np.array([[2, 3], [3, 1/2]])
G = nash.Game(A, B)

equilibria = G.support_enumeration()
for eq in equilibria:
    print(eq, np.sum(G[eq]))
