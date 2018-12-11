# Copyright 2016 Xinyi Wang All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 17:47:13 2018

@author: wangxinyi
"""

import time
from random import choice
from zmq.sugar.constants import found

class Node:
    def __init__(self,s, p = None, m = None):
        self.s = s
        self.p = p
        self.m = m
    def __repr__(self):
        h = self.s
        i = self.p
        print(i, h)
        
class SBP:
    def loadState(self, fn):
        fileName = fn
        f = open(fileName,'r')
        a = f.readline().strip().split(",")
        w,h = int(a[0]),int(a[1])
        lst = [ [0 for i in range(w)] for i in range(h) ]
        for i in range(h):
            a = f.readline().strip().split(",")
            for j in range(w):
                lst[i][j] = int(a[j])
        return lst
    
    def display(self,s):
        w,h = len(s[0]),len(s)
        print(str(w) + "," + str(h))
        for i in range(h):
            for j in range(w):
                print(s[i][j], end = ",")
            print()
            
    def clone(self,s):
        w,h = len(s[0]),len(s)
        cloneState = [[0 for x in range(w)] for y in range(h)]
        for i in range(h):
            for j in range(w):
                cloneState[i][j] = s[i][j]
        return cloneState

    def completeCheck(self,s):
        w,h = len(s[0]),len(s)
        for i in range(h):
            for j in range(w):
                if s[i][j] == -1:
                    return False
        return True
    
    def sCompare(self,s1,s2):
        w,h = len(s1[0]),len(s1)
        if w != len(s2[0]) or h != len(s2):
            return False
        else:
            for i in range(h):
                for j in range(w):
                    if s1[i][j] != s2[i][j]:
                        return False
        return True

    def normalize(self,s):
        s = self.clone(s)
        nextIdx = 3
        w,h = len(s[0]),len(s)
        for i in range(h):
            for j in range(w):
                if s[i][j] == nextIdx:
                    nextIdx += 1
                elif s[i][j] > nextIdx:
                    self.swapIdx(s,s[i][j],nextIdx)
                    nextIdx +=1
        return s
    
    def swapIdx(self,s,idx1,idx2):
        w,h = len(s[0]),len(s)
        for i in range(h):
            for j in range(w):
                if s[i][j] == idx1:
                    s[i][j] = idx2
                elif s[i][j] == idx2:
                    s[i][j] = idx1
        return
    
    def displayDirction(self,m):
        idx = m[0]
        dirt = m[1]
        if dirt == "r":
            print("({0},right)".format(idx))
        elif dirt == "l":
            print("({0},left)".format(idx))
        elif dirt == "u":
            print("({0},up)".format(idx))
        else:
            print("({0},down)".format(idx))


class Move:

    def indexS(self,s,p):
        w = len(s[0])
        h = len(s)
        l = []
        for i in range(h):
            for j in range(w):
                if s[i][j] == p:
                    l.append([i,j])
        topLeft = l[0]
        lowerRight = l[-1]
        width = lowerRight[1] - topLeft[1] + 1
        height = lowerRight[0] - topLeft[0] + 1
        lst = [topLeft,width,height]
        return lst

    def checkLeft(self,s,i,j,h):
        p = s[i][j]
        if p == 2:
            flag = 0
            for x in range(h):
                if s[i+x][j-1] == -1:
                    tmp = -1
                    if flag == 0:
                        flag = -1
                    elif tmp != flag:
                        return False
                elif s[i+x][j-1] == 0:
                    tmp = 1
                    if flag == 0:
                        flag = 1
                    elif tmp != flag:
                        return False
                else:
                    return False
            else:
                for x in range(w):
                    if s[i+1][j+x] != 0:
                        return False
            return True

    def checkRight(self,s,i,j,h):
        p = s[i][j]
        if p == 2:
            flag = 0
            for x in range(h):
                if s[i-x][j+1] == -1:
                    tmp = -1
                    if flag == 0:
                        flag = -1
                    elif tmp != flag:
                        return False
                elif s[i-x][j+1] == 0:
                    tmp = 1
                    if flag == 0:
                        flag = 1
                    elif tmp != flag:
                        return False
                else:
                    return False
        else:
            for x in range(h):
                if s[i-x][j+1] != 0:
                    return False
        return True

    def checkUp(self,s,i,j,w):
        p = s[i][j]
        if p == 2:
            flag = 0
            for x in range(w):
                if s[i-1][j+x] == -1:
                    tmp = -1
                    if flag == 0:
                        flag = -1
                    elif tmp != flag:
                        return False
                elif s[i-1][j+x] == 0:
                    tmp = 1
                    if flag == 0:
                        flag = 1
                    elif tmp != flag:
                        return False
                else:
                    return False
        else:
            for x in range(w):
                if s[i-1][j+x] != 0:
                    return False
        return True

    def checkDown(self,s,i,j,w):
        p = s[i][j]
        if p == 2:
            flag = 0
            for x in range(w):
                if s[i+1][j-x] == -1:
                    tmp = -1
                    if flag == 0:
                        flag = -1
                    elif tmp != flag:
                        return False
                elif s[i+1][j-x] == 0:
                    tmp = 1
                    if flag == 0:
                        flag = 1
                    elif tmp != flag:
                        return False
                else:
                    return False
        else:
            for x in range(w):
                if s[i+1][j-x] != 0:
                    return False
        return True

    def allMove(self,s):
        lst = {}
        allmove = []
        h = len(s)
        w = len(s[0])
        maxIndex = 1
        for i in range(h):
            for j in range(w):
                if maxIndex < s[i][j]:
                    maxIndex = s[i][j]
        for i in range(2,maxIndex+1):
            lst[i] = self.allMoveSP(s, i)
        for i in lst:
            for j in range( len(lst[i]) ):
                allmove.append(( i,lst[i][j] ))
        return allmove

    def allMoveSP(self,s,p):
        l = self.indexS(s,p)
        topLeft = l[0]
        width = l[1]
        height = l[2]
        lowerRight = [l[0][0]+height-1, l[0][1]+width-1]
        lst = []
        if self.checkLeft(s, topLeft[0], topLeft[1], height):
            lst.append("l")
        if self.checkRight(s, lowerRight[0], lowerRight[1], height):
            lst.append("r")
        if self.checkUp(s, topLeft[0], topLeft[1], width):
            lst.append("u")
        if self.checkDown(s, lowerRight[0], lowerRight[1], width):
            lst.append("d")
        return lst

    def applyMove(self,s,m):
        piece = m[0]
        direction = m[1]
        lst = self.allMoveSP(s, piece)
        [topLeft, width, height] = self.indexS(s, piece)
        i = topLeft[0]
        j = topLeft[1]
        if direction in lst:
            if direction == "l":
                for x in range(height):
                    s[i+x][j-1],s[i+x][j+width-1] = piece,0     
            elif direction == "r":
                for x in range(height):
                    s[i+x][j+width],s[i+x][j] = piece,0
            elif direction == "u":
                for x in range(width):
                    s[i-1][j+x],s[i+height-1][j+x] = piece,0
            else:
                for x in range(width):
                    s[i+height][j+x],s[i][j+x] = piece,0
        else:
            print("The piece you selected cannot be moved in this direction.")
            return s
        
        def applyMovingCloning(self,s,m):
            sbp = SBP()
            state = sbp.clone(s)
            return self.applyMove(state, m)

    def randomWalks(self,s,N):
        sbp = SBP()
        sbp.display(s)
        print()
        while(N):
            lst = self.allMove(s)
            move = choice(lst)
            self.applyMove(s, move)
            sbp.displayDirction(move)
            print()
            sbp.display(s)
            print()
            if sbp.completeCheck(s):
                print("Move {0} times to reach goal!".format(N))
                return
            N = N-1
            return

    def bfs(self,s):
        start = time.clock()
        sbp = SBP()
        queue = []
        visited = []
        queue.append(Node(s))
        visited.append(s)
        while queue:
            sNode = queue.pop(0)
            if sbp.completeCheck(sNode.s):
                current = sNode
                lst = []
                while current.p != None:
                    lst.append(current.m)
                    current = current.p
                soluLength = len(lst)
                while lst:
                    a = lst.pop()
                    sbp.displayDirction(a)
                sbp.display(sNode.s)
                elapse = time.clock() - start
                print("Explore {0} nodes, {1} seconds, length:{2}".format(len(visited), elapse, soluLength))
                return sNode
            else:
                dirLst = self.allMove(sNode.s)
                for i in dirLst:
                    tmp = self.applyMovingCloning(sNode.s,i)
                    t = sbp.normalize(tmp)
                    if t not in visited:
                        tmp = Node(tmp,sNode,i)
                        queue.append(tmp)
                        visited.append(t)
        print("Cannot reach to goal!")
        return

    def dfs(self,s):
        start = time.clock()
        sbp = SBP()
        stack = []
        visited = []
        stack.append(Node(s))
        visited.append(s)
        while stack:
            sNode = stack[-1]
            if sbp.completeCheck(sNode.s):
                current = sNode
                dirLst = []
                while current.p != None:
                    dirLst.append(current.m)
                    current = current.p
                soluLength = len(dirLst)
                while dirLst:
                    sbp.displayDirction(dirLst.pop())
                sbp.display(sNode.s)
                elapse = time.clock() - start
                print("Explore {0} nodes, {1} seconds, length:{2}".format(len(visited), elapse, soluLength))
                return sNode
            else:
                flag = 0
                dirLst = self.allMove(sNode.s)
                for m in dirLst:
                    tmp = self.applyMovingCloning(sNode.s, m)
                    t = sbp.normalize(tmp)
                    if t not in visited:
                        stack.append(Node(tmp, sNode, m))
                        visited.append(t)
                        flag = 1
                        break
                if flag == 0:
                    stack.pop()
        print("Cannot reach to goal!")
        return

    def iddfs(self,s,maxDepth):
        start = time.clock()
        for i in range(1,maxDepth):
            lst = self.dls(s,i)
            if lst == None:
                continue
            else:
                found = lst[0]
                expNodes = lst[1]
            current = found
            dirLst = []
            while current.p != None:
                dirLst.append(current.m)
                current = current.p
            soluLength = len(dirLst)
            while dirLst:
                sbp.displayDirction(dirLst.pop())
            sbp.display(found.s)
            elapse = time.clock() - start
            print("Explore {0} nodes, {1} seconds, length:{2}".format(expNodes, elapse, soluLength))
            return found
        print("Cannot reach goals with given depth!")
        return
    
    def dls(self,s,depth):
        sbp = SBP()
        stack = []
        visited = []
        stack.append(Node(s))
        visited.append(s)
        N = 0
        while stack:
            N += 1
            sNode = stack[-1]
            if sbp.completeCheck(sNode.s):
                return [sNode,len(visited)]
            else:
                flag = 0
                dirLst = self.allMove(sNode.s)
                for m in dirLst:
                    tmp = self.applyMovingCloning(sNode.s, m)
                    t = sbp.normalize(tmp)
                    if t not in visited:
                        stack.append(Node(tmp, sNode, m))
                        visited.append(t)
                        flag = 1
                        break
                if N == depth or flag == 0:
                    stack.pop()
                    N -= 1
        return None

sbp = SBP()
move = Move()
s = sbp.loadState("E:/Intro to Artificial Intel/hw/HW1/SBP-level0.txt")
s1 = sbp.loadState("E:/Intro to Artificial Intel/hw/HW1/SBP-level1.txt")
move.randomWalks(s, 3)
print("This is the solution using breadth-first search:")
move.bfs(s1)
print()
print("This is the solution using depth-first search:")
move.dfs(s1)
print()
print("This is the solution using iterative deepening
search:")
move.iddfs(s1,10000000000000)
