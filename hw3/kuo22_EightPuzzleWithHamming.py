''' kuo22_AStar.py
By Kuo Hong
CSE 415 Assignment 3

The implementation for Hamming heuristic. Checks for tiles out of place.
'''
from EightPuzzle import *

GOAL = [[0,1,2],
        [3,4,5],
        [6,7,8]]

# For every tile that's blank, check if it's out of place 
# and add to total h
def h(s):
    h = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != 0 and s.b[i][j] != GOAL[i][j]:
                h += 1
    return h
            
