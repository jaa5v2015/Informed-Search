#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#a-star



import heapq
import sys
import fileinput
import random
import copy
import subprocess


class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

nodeid = 0
class node():
    def __init__(self,val):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.val = val
        self.parent = None
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)

    

class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet


class state():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0,1,2],[3,4,5],[6,7,8]]

               
        
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

def h0():
    h = 0
    return h

def h1(goal,start):
        row = 3
        col = 3
        h= 0
        for r in range(row):
            for c in range(col):
                if(goal.tiles[r][c] != start.tiles[r][c]):
                    h += 1
        return h
def h2(goal,start):
        h = 0 
        for i in range(3):
            for j in range(3):
                x, y = divmod(start.tiles[i][j],3)
                h += abs(x -i) + abs(y-j)
        return h
     
    
def h3(goal,start):
        row = 3
        col = 3
        h= 0
        for r in range(row):
            for c in range(col):
                if(goal.tiles[r][c] == start.tiles[r][c]):
                    h += 1
        return h
def main():
    input = sys.stdin.read(); input = input.split()
    goal = state()
    current_state = state()
    
    #Gets random board from random_board.py and makes it your start state
    i = 0
    for rows in range(len(current_state.tiles)):
        for cols in range(len(current_state.tiles[rows])):
            current_state.tiles[rows][cols] = int(input[i])
            i+=1
            if(current_state.tiles[rows][cols] == 0):
                current_state.xpos = rows
                current_state.ypos = cols
    
    
    # random board = current node
    
    #Variable declarations 
    closed_list = Set()
    open_list = PriorityQueue()
    state_closedList = []
    state_openList = []
    h = 0
    g = 0
    h_choice = 0
    t = True
    
    #Variables needed for paper
    V = 0 #Number of nodes visted/expanded
    N = 0 #The max number of nodes stored in memory (closed list + open list)
    d = 0 #depth of the optimal souloution
    b = 0  #approximate- effective branching factor (b) where N = b^d
    optimal_path = [] #list to hold the optimal path
    
    # Hueristic 0
    if sys.argv[1] == "0":
        h = 0
        h_goal = 0
        h_choice = 0
    
    #Number of misplaced tiles
    elif sys.argv[1] == "1":
        h = h1(goal,current_state)
        h_goal = h1(goal,goal)
        h_choice = 1
        
        
    # Manhatten    
    elif sys.argv[1] == "2":
        h = h2(goal,current_state)
        h_goal = h2(goal, goal)
        h_choice = 2
    
    #number of tiles in the right place
    elif sys.argv[1] == "3":
        h = h3(goal,current_state)
        h_goal = h3(goal,goal)
        h_choice = 3
        
    
    #F-value
    f = g + h
    f_goal = g + h_goal
    

    # A-star algorithm
    start_node = node(f)
    goal_node = node(f_goal)
    
    
    #add start node to the open list
    open_list.push(start_node)
    state_openList.append(current_state)
    
    
    #t = True
    while t == True:
        current_node = open_list.pop()
        current_state = state_openList[current_node.id - 1]
        
        if current_state.tiles != goal.tiles:
            
            closed_list.add(current_node)
            state_closedList.append(current_state)
        
        
            #Generate children of current state
            child_up = current_state.up()
            child_down = current_state.down()
            child_left = current_state.left()
            child_right = current_state.right()
        
            #Check to see if children are on the closed list
            #if not on the closed list add to the open list
            g += 1
            if(closed_list.isMember(child_up) == False) and (child_up != None):
                if h_choice == 0:
                    h = 0
                elif h_choice == 1:
                    h = h1(goal,child_up)
                elif h_choice == 2:
                    h = h2(goal,child_up)
                elif h_choice == 3:
                    h = h3(goal,child_up)
                f = g + h
                child_node = node(f)
                child_node.parent = current_node
                open_list.push(child_node)
                state_openList.append(child_up)
        
            if(closed_list.isMember(child_down)== False) and (child_down != None):
                if h_choice == 0:
                    h = 0
                elif h_choice == 1:
                    h = h1(goal,child_down)
                elif h_choice == 2:
                    h = h2(goal,child_down)
                elif h_choice == 3:
                    h = h3(goal,child_down)
                f = g + h
                child_node = node(f)
                child_node.parent = current_node
                open_list.push(child_node)
                state_openList.append(child_down)
        
            if(closed_list.isMember(child_left) == False) and (child_left != None):
                if h_choice == 0:
                    h = 0
                elif h_choice == 1:
                    h = h1(goal,child_left)
                elif h_choice == 2:
                    h = h2(goal,child_left)
                elif h_choice == 3:
                    h = h3(goal,child_left)
                f = g + h
                child_node = node(f)
                child_node.parent = current_node
                open_list.push(child_node)
                state_openList.append(child_left)
            
            if(closed_list.isMember(child_right) == False) and (child_right != None):
                if h_choice == 0:
                    h = 0
                elif h_choice == 1:
                    h = h1(goal,child_right)
                elif h_choice == 2:
                    h = h2(goal,child_right)
                elif h_choice == 3:
                    h = h3(goal,child_right)
                f = g + h
                child_node = node(f)
                child_node.parent = current_node
                open_list.push(child_node)
                state_openList.append(child_right)
            
    
        else:
            closed_list.add(current_node)
            state_closedList.append(current_state)
            
            
            
            
            
            while current_node.parent != None:
                optimal_path.append(state_openList[current_node.id-1])
                current_node = current_node.parent
            
            len_of_path = len(optimal_path)
            optimal_path_dist = len(optimal_path)
            
            #total number of nodes visted
            V = (closed_list.length())
            print("V = ", V)
        
            #number of total nodes stored in memory
            op = open_list.length()
            N = V + op
            print("N = ",N)
            
            #Depth of optimal path
            d = optimal_path_dist + 1
            print("d = ",d)
            
            #Branching factor
            new_d = 1 / d
            b = N**new_d
            print("b = ", b)
            
             
            print(state_openList[current_node.id])
            
            while len_of_path != 0:
                print(optimal_path[len_of_path - 1])
                len_of_path -= 1
            
            t = False
        
          
    
main()