'''Missionaries.py
("Missionaries and Cannibals" problem)
'''
#<METADATA>
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "Missionaries and Cannibals"
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
          'grain':LEFT, 
          'boat':LEFT 
        }
    self.d = d

  def __eq__(self,s2):
    for prop in ['farmer', 'fox', 'chicken', 'grain', 'boat']:
      if self.d[prop] != s2.d[prop]: 
        return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = 'Farmer: ' + SIDE[self.d['farmer']] + '\n'
    txt += 'Fox: ' + SIDE[self.d['fox']] + '\n'
    txt += 'Chicken: ' + SIDE[self.d['chicken']] + '\n'
    txt += 'Grain: ' + SIDE[self.d['grain']] + '\n'
    txt += 'Boat: ' + SIDE[self.d['boat']] + '\n'

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
    news.d['boat'] = self.d['boat']

    # news.d['people']=[self.d['people'][M_or_C][:] for M_or_C in [M, C]]
    # news.d['boat'] = self.d['boat']
    return news 

  def can_move(self, p=None):
    side = self.d['farmer']
    if self.d['farmer'] != self.d['boat']:
      return False
    if p == None:
      if (self.d['fox'] == side and self.d['chicken']) or (self.d['chicken'] == side and self.d['grain'] == side):
        return False
    if p == 'fox' and self.d['chicken'] == side and self.d['grain'] == side:
      return False
    if p == 'grain' and self.d['fox'] == side and self.d['chicken'] == side:
      return False 
    
    return True


  def move(self,m,c):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['boat']         # where is the boat?
    p = news.d['people']          # get the array of arrays of people.
    p[M][side] = p[M][side]-m     # Remove people from the current side.
    p[C][side] = p[C][side]-c
    p[M][1-side] = p[M][1-side]+m # Add them at the other side.
    p[C][1-side] = p[C][1-side]+c
    news.d['boat'] = 1-side       # Move the boat itself.
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
CREATE_INITIAL_STATE = lambda : State(d={'farmer':LEFT, 'fox':LEFT, 'chicken':LEFT, 'grain':LEFT, 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
MC_combinations = [(1,0),(2,0),(3,0),(1,1),(2,1)]

OPERATORS = [Operator(
  "Cross the river with "+str(m)+" missionaries and "+str(c)+" cannibals",
  lambda s, m1=m, c1=c: s.can_move(m1,c1),
  lambda s, m1=m, c1=c: s.move(m1,c1) ) 
  for (m,c) in MC_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
