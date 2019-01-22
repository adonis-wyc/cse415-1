'''IDDFS.py
by Kuo Hong

Assignment 2, in CSE 415, Winter 2019.
 
This file contains my search algorithm for iterative deepening
depth-first search.
'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to IDDFS")
COUNT = None
BACKLINKS = {}

def runIDDFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    IDDFS(initial_state)
    print(str(COUNT)+" states expanded.")
    print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IDDFS(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    MAX_DEPTH = 0
    BACKLINKS[initial_state] = None
    NO_NEXT_LEVEL = False 
    CLOSED = []
    # Stops running if there are no more unvisited legal moves
    while not NO_NEXT_LEVEL:
      # STEP 1. Put the start state on a list OPEN
      OPEN = [initial_state]
      # If not first time in loop, add all deepest visited nodes to OPEN
      if MAX_DEPTH > 0:
        OPEN = []
        for s in BACKLINKS:
          if BACKLINKS[s] != None and BACKLINKS[s][1] == MAX_DEPTH - 1:
            OPEN.append(s)
      NO_NEXT_LEVEL = True

      # STEP 2. If OPEN is empty, output “DONE” and stop.
      while OPEN != []:
        report(OPEN, CLOSED, COUNT)
        if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

        # STEP 3. Select the first state on OPEN and call it S.
        #         Delete S from OPEN.
        #         Put S on CLOSED.
        #         If S is a goal state, output its description
        S = OPEN.pop(0)
        level = 0
        if BACKLINKS[S] != None:
            level = BACKLINKS[S][1] + 1
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            print('Length of solution path found: '+str(len(path)-1)+' edges')
            return
        COUNT += 1

        # STEP 4. Generate the list L of successors of S and delete 
        #         from L those states already appearing on CLOSED.
        L = []
        for op in Problem.OPERATORS:
          if op.precond(S):
            NO_NEXT_LEVEL = False
            if level <= MAX_DEPTH:
              new_state = op.state_transf(S)
              if not (new_state in CLOSED):
                L.append(new_state)
                if new_state not in BACKLINKS:
                    BACKLINKS[new_state] = [S, level]
        print(NO_NEXT_LEVEL)

        # STEP 5. Delete from OPEN any members of OPEN that occur on L.
        #         Insert all members of L at the front of OPEN.
        for s2 in L:
            for i in range(len(OPEN)):
                if (s2 == OPEN[i]):
                    del OPEN[i]; break

        OPEN = L + OPEN
        print_state_list("OPEN", OPEN)
        # STEP 6. Go to Step 2.
      MAX_DEPTH += 1

def print_state_list(name, lst):
  print(name+" is now: ",end='')
  if lst == []:
    print('Empty')
  else:
    for s in lst[:-1]:
      print(str(s),end=', ')
    print(str(lst[-1]))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    if BACKLINKS[S] != None:
      S = BACKLINKS[S][0]
    else:
      S = None
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path    
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()

