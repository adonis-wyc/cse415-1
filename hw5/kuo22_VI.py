'''kuo22_VI.py

Value Iteration for Markov Decision Processes.
'''

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
   return "Kuo Hong" # For an autograder.

Vkplus1 = {}
Q_Values_Dict = {}

def one_step_of_VI(S, A, T, R, gamma, Vk):
   '''S is list of all the states defined for this MDP.
   A is a list of all the possible actions.
   T is a function representing the MDP's transition model.
   R is a function representing the MDP's reward function.
   gamma is the discount factor.
   The current value of each state s is accessible as Vk[s].
   '''
   global Vkplus1, Q_Values_Dict
   Vkplus1 = {}
   Q_Values_Dict = {}
   # For each (s, a, sp) combination, add its Q value to the Q Dictionary.
   for s in S:
      for a in A:
         for sp in S:
            partial_Q = T(s, a, sp) * (R(s, a, sp) + gamma * Vk[sp])
            if (s, a) not in Q_Values_Dict:
               Q_Values_Dict[(s, a)] = partial_Q
            else:
               Q_Values_Dict[(s, a)] += partial_Q
   
   # Check all Q States and update Vkplus1 for that state whenever the Q value is greater.
   for (s, a) in Q_Values_Dict:
      if s not in Vkplus1:
         Vkplus1[s] = Q_Values_Dict[(s, a)]
      elif Q_Values_Dict[(s, a)] > Vkplus1[s]:
         Vkplus1[s] = Q_Values_Dict[(s, a)]
   
   # Check Vkplus1 against the given Vk and find the delta max value.
   delta_max = 0
   for s in Vkplus1:
      if abs(Vkplus1[s] - Vk[s]) > delta_max:
         delta_max = abs(Vkplus1[s] - Vk[s])
   

   '''Your code should fill the dictionaries Vkplus1 and Q_Values_dict
   with a new value for each state, and each q-state, and assign them
   to the state's and q-state's entries in the dictionaries, as in
       Vkplus1[s] = new_value
       Q_Values_Dict[(s, a)] = new_q_value

   Also determine delta_max, which we define to be the maximum
   amount that the absolute value of any state's value is changed
   during this iteration.
   '''
   
   return (Vkplus1, delta_max)
   #return (Vk, 0) # placeholder

def return_Q_values(S, A):
   '''Return the dictionary whose keys are (state, action) tuples,
   and whose values are floats representing the Q values from the
   most recent call to one_step_of_VI. This is the normal case, and
   the values of S and A passed in here can be ignored.
   However, if no such call has been made yet, use S and A to
   create the answer dictionary, and use 0.0 for all the values.
   '''
   global Q_Values_Dict
   # If no Q values not set, set them to 0 using the given S and A
   if not Q_Values_Dict:
      for s in S:
         for a in A:
            Q_Values_Dict[(s, a)] = 0.0
   
   return Q_Values_Dict

Policy = {}
def extract_policy(S, A):
   '''Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.  If none have yet been
   computed, call return_Q_values to initialize q-values, and then
   extract a policy.  Ties between actions having the same (s, a) value
   can be broken arbitrarily.
   '''
   global Policy
   Q_values = return_Q_values(S, A)
   Q_max = {}
   Policy = {}
   # Find the action with the highest value in the Q value dictionary
   for s, a in Q_values:
      if s not in Policy:
         Policy[s] = a 
         Q_max[s] = Q_values[(s, a)]
      elif Q_values[(s, a)] > Q_max[s]:
         Policy[s] = a
         Q_max[s] = Q_values[(s, a)]

   return Policy

def apply_policy(s):
   '''Return the action that your current best policy implies for state s.'''
   global Policy
   return Policy[s]

   # return None # placeholder


