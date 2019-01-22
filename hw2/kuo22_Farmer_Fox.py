'''kuo22_Farmer_Fox.py
by Kuo Hong

Assignment 2, in CSE 415, Winter 2019.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
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
 '''The Farmer and Fox problem starts with the farmer, fox, chicken, and grain on the left side of a river. 
 The goal is to transport everything to the right side using a boat. The boat must be rowed by the farmer
 and he can only carry one thing with him at a time. The fox will eat the chicken 
 and the chicken will eat the grain if left alone by the farmer. 
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
    txt = 'Left: '
    txt2 = '\nRight: '
    for prop in ['farmer', 'fox', 'chicken', 'grain']:
      if self.d[prop] == LEFT:
        txt += prop + ' '
      else:
        txt2 += prop + ' '

    return txt + txt2 + '\n'

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