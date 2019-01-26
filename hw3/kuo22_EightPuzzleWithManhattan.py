from EightPuzzle import *

def h(s):
    h = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != 0:
                num = s.b[i][j]
                goal_row = int (num / 3)
                goal_col = num % 3
                dist = abs(i - goal_row) + abs(j - goal_col)
                h += dist
    # print(str(h))
    return h
