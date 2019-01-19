'''Missionaries.py
("Missionaries and Cannibals" problem)
'''
#<METADATA>
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "Farmer and Fox"
PROBLEM_VERSION = "2.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "07-JAN-2018"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Missionaries and Cannibals"</b> problem is a traditional puzzle
in which the player starts off with three missionaries and three cannibals
on the left bank of a river.  The object is to execute a sequence of legal
moves that transfers them all to the right bank of the river.  In this
version, there is a boat that can carry at most three people, and one of
them must be a missionary to steer the boat.  It is forbidden to ever
have one or two missionaries outnumbered by cannibals, either on the
left bank, right bank, or in the boat.  In the formulation presented
here, the computer will not let you make a move to such a forbidden situation, and it
will only show you moves that could be executed "safely."
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.

SIDE = {
  0: 'left',
  1: 'right'
}

class State():

  def __init__(self, d=None):
    if d==None: 
      d = {
          'farmer':LEFT,
          'fox':LEFT,
          'chicken':LEFT, 
          'grain':LEFT
        }
    self.d = d

  def __eq__(self,s2):
    for prop in ['farmer', 'fox', 'chicken', 'grain']:
      if self.d[prop] != s2.d[prop]: 
        return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = '\nFarmer: ' + SIDE[self.d['farmer']] + '\n'
    txt += 'Fox: ' + SIDE[self.d['fox']] + '\n'
    txt += 'Chicken: ' + SIDE[self.d['chicken']] + '\n'
    txt += 'Grain: ' + SIDE[self.d['grain']] + '\n'

    # p = self.d['people']
    # txt = "\n M on left:"+str(p[M][LEFT])+"\n"
    # txt += " C on left:"+str(p[C][LEFT])+"\n"
    # txt += "   M on right:"+str(p[M][RIGHT])+"\n"
    # txt += "   C on right:"+str(p[C][RIGHT])+"\n"
    # side='left'
    # if self.d['boat']==1: side='right'
    # txt += " boat is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['farmer'] = self.d['farmer']
    news.d['fox'] = self.d['fox']
    news.d['chicken'] = self.d['chicken']
    news.d['grain'] = self.d['grain']

    # news.d['people']=[self.d['people'][M_or_C][:] for M_or_C in [M, C]]
    # news.d['boat'] = self.d['boat']
    return news 

  def can_move(self, p):
    side = self.d['farmer']
    if p == 'farmer':
      if (self.d['fox'] == side and self.d['chicken'] == side) or (self.d['chicken'] == side and self.d['grain'] == side):
        return False
    if p == 'fox' and (self.d['fox'] != side or (self.d['chicken'] == side and self.d['grain'] == side)):
      return False
    if p == 'grain' and (self.d['grain'] != side or (self.d['fox'] == side and self.d['chicken'] == side)):
      return False 
    if p == 'chicken' and self.d['chicken'] != side:
      return False
    
    return True


  def move(self, p):
    news = self.copy()
    side = self.d['farmer']
    news.d['farmer'] = 1 - side
    if p != 'farmer':
      news.d[p] = 1 - side

    return news

def goal_test(s):
  '''If all Ms and Cs are on the right, then s is a goal state.'''
  for prop in ['farmer', 'fox', 'chicken', 'grain']:
    if s.d[prop] == LEFT:
      return False
  return True

  # p = s.d['people']
  # return (p[M][RIGHT]==3 and p[C][RIGHT]==3)

def goal_message(s):
  return "Congratulations on successfully guiding the farmer gang across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'farmer':LEFT, 'fox':LEFT, 'chicken':LEFT, 'grain':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
combinations = ['farmer', 'fox', 'chicken', 'grain']
# MC_combinations = [(1,0),(2,0),(3,0),(1,1),(2,1)]

OPERATORS = [Operator(
  "Farmer crosses river with " + p + ".",
  lambda s, p1=p: s.can_move(p1),
  lambda s, p1=p: s.move(p1)) 
  for p in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>