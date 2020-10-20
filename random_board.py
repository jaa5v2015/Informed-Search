#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#Random Board

import sys
import fileinput
import random
import copy

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

input = sys.stdin.read(); input = input.split()
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




def main():

    #read file in from input
   # filein = open(sys.argv[1], "r")
    input = sys.stdin.read(); input = input.split()
   
            
##################    #Random seed and random moves###################################
    rand_seed = input("Enter the random seed")
    random.seed(rand_seed)
    #random.seed(sys.argv[1])
    
    shuffled_2d = state()
    #num_of_moves = int(sys.argv[2])
    num_of_moves = input("Enter the number of random moves: ")
    
    move = random.randrange(4)
    moves_count = 0
    while moves_count < num_of_moves:
        if move == 0:
            if(shuffled_2d.right() != None):
                shuffled_2d = shuffled_2d.right()
                moves_count += 1
                 
        elif move == 1:
            if(shuffled_2d.down() != None):
                shuffled_2d = shuffled_2d.down()
                moves_count += 1
                
        elif move == 2:
            if(shuffled_2d.left() != None):
                shuffled_2d = shuffled_2d.left()
                moves_count += 1
                
        elif move == 3:
            if(shuffled_2d.up() != None):
                shuffled_2d = shuffled_2d.up()
                moves_count += 1
                
        move = random.randrange(4)
        #return shuffled_2d
    
    print(shuffled_2d)
    
                               
main()


    
        



