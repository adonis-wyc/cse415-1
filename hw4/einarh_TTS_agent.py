'''einarh_TTS_agent.py
My agent that plays Toro-Tile Straight.

***
I have implemented both options under Interesting utterances, for the extra credit.
***
'''

# TODO:
# Optimise eval for a multiple row play
# How do we do minmax when we reach a terminating condition that is not max_depth?
from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

CUR_K = 5
CUR_PLAYER = "W"
CUR_OTHER_PLAYER = "player2"
CUR_CACHE = {}

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    global CUR_K
    white_val = self.calc_c("W", 2, CUR_K)
    black_val = self.calc_c("B", 2, CUR_K)

    return white_val - black_val
  
  def efficienct_calc_c(self):
    global CUR_K, CUR_CACHE
    if self in CUR_CACHE:
      return CUR_CACHE[self]
    sum = 0
    res_white = self.efficient_calc_c_helper('W', CUR_K)
    # print(res_white)
    res_black = self.efficient_calc_c_helper('B', CUR_K)
    for i in range(0, CUR_K):
      sum += (res_white[i]-res_black[i]) * (10**(i))
    CUR_CACHE[self] = sum
    return sum

  def efficient_calc_c_helper(self, player, k):
    global CUR_K
    K = CUR_K
    # print("K,",K)
    res = [0 for _ in range(K)]

    # calc_count = 0
    # Iterate through all squares on board
    for row_idx in range(len(self.board)):
      for col_idx in range(len(self.board[0])):
        val = self.board[row_idx][col_idx]
        if val == swap_player(player) or val == "-":
          continue
        
        # For each square, check each of four (of eight) directions

        # Up
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = col_idx
          temp_row = (row_idx - i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if valid_row:
          for j in range(1,K+1):
            if count_color_in_row == j:
              res[j-1] += 1
              # print("Up", row_idx, col_idx, player, count_color_in_row)

        # if count_color_in_row == count and valid_row:
        #   calc_count += 1
          # print("Up", row_idx, col_idx, player, count)

        # Up-right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = (row_idx - i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if valid_row:
          for j in range(1,K+1):
            if count_color_in_row == j:
              res[j-1] += 1
              # print("Up-right", row_idx, col_idx)

        # if count_color_in_row == count:
        #   calc_count += 1
          # print("Up-right", row_idx, col_idx)

        # Right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = row_idx
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if valid_row:
          for j in range(1,K+1):
            if count_color_in_row == j:
              res[j-1] += 1
              # print("Right", row_idx, col_idx)

        # if count_color_in_row == count:
        #   calc_count += 1
          # print("Right", row_idx, col_idx)

        # Down-right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = (row_idx + i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if valid_row:
          for j in range(1,K+1):
            if count_color_in_row == j:
              res[j-1] += 1
              # print("Down-Right", row_idx, col_idx)
        # if count_color_in_row == count:
        #   calc_count += 1


    return res

    

    # for i in range(0, K):
    #   white_val = self.calc_c("W", K-i, K)
    #   # print("White val", K-i, white_val)
    #   black_val = self.calc_c("B", K-i, K)
    #   # print("Black val", K-i, black_val)

    #   sum += (white_val-black_val) * (10**(K-i))

  def calc_c(self, player, count, k):
    calc_count = 0
    # Iterate through all squares on board
    for row_idx in range(len(self.board)):
      for col_idx in range(len(self.board[0])):
        val = self.board[row_idx][col_idx]
        if val == swap_player(player) or val == "-":
          continue
        
        # For each square, check each of four (of eight) directions

        # Up
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = col_idx
          temp_row = (row_idx - i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if count_color_in_row == count and valid_row:
          calc_count += 1
          # print("Up", row_idx, col_idx, player, count)

        # Up-right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = (row_idx - i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if count_color_in_row == count and valid_row:
          calc_count += 1
          # print("Up-right", row_idx, col_idx)

        # Right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = row_idx
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if count_color_in_row == count and valid_row:
          calc_count += 1
          # print("Right", row_idx, col_idx)

        # Down-right
        valid_row = True
        count_color_in_row = 0
        for i in range(k):
          temp_col = (col_idx + i) % len(self.board[0])
          temp_row = (row_idx + i) % len(self.board)
          temp_val = self.board[temp_row][temp_col]
          if temp_val == player:
            count_color_in_row += 1
          elif temp_val != ' ':
            valid_row = False
            break
        if count_color_in_row == count and valid_row:
          calc_count += 1
          # print("Down-right", row_idx, col_idx)

    return calc_count 


  def custom_static_eval(self):
    # Reward positions that allow for a win via multiple columns
    return self.efficienct_calc_c()
    global CUR_K
    K = CUR_K
    # print("K,",K)
    sum = 0
    for i in range(0, K):
      white_val = self.calc_c("W", K-i, K)
      # print(white_val)
      # print("White val", K-i, white_val)
      black_val = self.calc_c("B", K-i, K)
      # print("Black val", K-i, black_val)

      sum += (white_val-black_val) * (10**(K-i-1))
    return sum


def take_turn(current_state, last_utterance, time_limit):

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    
    
    # Place a new tile
    location = _find_next_move(new_state, time_limit)
    # location = _find_next_vacancy(new_state.board)
    if location==False: return [[False, current_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = current_state.whose_turn

    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = generate_utterance(new_state, last_utterance, who)

    return [[move, new_state], new_utterance]

utterance_cycle = 0
feature_cycle = 0
def generate_utterance(state, last_utterance, who):
    global utterance_cycle, feature_cycle, CUR_K
    k = CUR_K
    utterances = [
      'Meow, that was a good move. By me.',
      'Purr, I can\'t wait for my nap once I\'ve defeated you.',
      'Hisss, that was a tough one.',
      'Psh, this is too easy.',
      'Can you believe you\'re about to lose to a cat!? How embarassing.',
      'Here\'s my move, now hold on while I go play with my yarn.',
      'Meow, you must be glad your friends aren\'t here to see this.',
      'Purrr, here\'s my move.',
      'Hisss, how do you like that?',
      'I\'m ready for my nap, so let me wrap this up and beat you.'
    ]
    new_utterance_first = utterances[utterance_cycle%len(utterances)]
    utterance_cycle += 1

    if feature_cycle == 0:
      new_utterance_second = "Look at this, according to my calculations, the state of our board is {}.".format(state.custom_static_eval())
    elif feature_cycle == 1:
      cur_player = who
      k_minus_1 = state.calc_c(cur_player, k-1, k)
      k_minus_2 = state.calc_c(cur_player, k-2, k)
      new_utterance_second = "Meow, I have {} {}'s in a row and {} {}'s in a row.".format(k_minus_1, (k-1), k_minus_2, (k-2))
    else:
      new_who = 'B'  
      if who=='B': new_who = 'W'  
      other_player = new_who
      k_minus_1 = state.calc_c(other_player, k-1, k)
      k_minus_2 = state.calc_c(other_player, k-2, k)
      new_utterance_second = "Meow, you have {} {}'s in a row and {} {}'s in a row.".format(k_minus_1, (k-1), k_minus_2, (k-2))
    
    feature_cycle = (feature_cycle + 1) % 3
    
    return new_utterance_first + " " + new_utterance_second
  
def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def _find_next_move(state, time_limit):
    current_state = state
    use_default_move_ordering = True
    use_custom_static_eval_function = True
    use_iterative_deepening_and_time = True
    alpha_beta = True
    time_limit = time_limit
    max_ply = 3
    results = parameterized_minimax_helper(
       current_state,
       use_iterative_deepening_and_time,
       max_ply,
       use_default_move_ordering,
       alpha_beta, 
       time_limit,
       use_custom_static_eval_function)
    # Note: What happens if there is no next move?
    return results[5]

def moniker():
    return "Winston" # Return your agent's short nickname here.

def who_am_i():
    return """My name is Winston the Cat, created by Einar (einarh).
I am a champion mouse-chaser and takes naps whenever I please. 
I can beat you at TTS in my sleep."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global CUR_K, CUR_PLAYER, CUR_OTHER_PLAYER
    CUR_K = k
    CUR_PLAYER = who_i_play
    CUR_OTHER_PLAYER = player2Nickname
    return "OK"

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
  '''This function will spawn a thread and run the given function using the args, kwargs and 
  return the given default value if the timeout_duration is exceeded 
  ''' 
  import threading
  import sys
  import time
  class MinimaxThread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      self.result = default
    def run(self):
      try:
        self.result = func(*args, **kwargs)
      except Exception as e:
        print("The agent threw an exception, or there was a problem with the time.")
        print(sys.exc_info())
        print(e[2])
        self.result = default

  pt = MinimaxThread()
  pt.start()
  started_at = time.time()
  # print("take_turn started at: " + str(started_at))
  pt.join(timeout_duration)
  ended_at = time.time()
  # print("take_turn ended at: " + str(ended_at))
  diff = ended_at - started_at
  print("Used %0.4f seconds in take_turn, out of %0.4f" % (diff, timeout_duration))
  if pt.isAlive():
    # print("still alive")
    return default
  else:
    # print("Within the time limit -- nice!")
    return pt.result



def parameterized_minimax_helper(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):
  time_limit -= 0.01
  import time
  start_time = time.perf_counter()

  vacancy = _find_next_vacancy(current_state.board)
  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
  # current_state_static_val = -1000.0
  # n_states_expanded = 0
  # n_static_evals_performed = 0
  # max_depth_reached = 0
  # n_ab_cutoffs = 0

  info = {
    "current_state_static_val": 0,
    "n_states_expanded": 0,
    "n_static_evals_performed": 0,
    "max_depth_reached": 0,
    "n_ab_cutoffs": 0
  }

  # STUDENTS: You may create the rest of the body of this function here.

  # if use_custom_static_eval_function:
  #   current_state_static_val = current_state.custom_static_eval()
  # else:
  #   current_state_static_val = current_state.static_eval()
    
  # Run DFS
  if use_iterative_deepening_and_time:
    cur_allowed_depth = 1
    best_move = vacancy
    while cur_allowed_depth <= max_ply:
      time_limit -= 0.01
      time_used = time.perf_counter() - start_time
      time_remaining = time_limit - time_used

      new_best_move, new_info = minimax(current_state, use_custom_static_eval_function, use_default_move_ordering,
                                 max_ply, info, alpha_beta, cur_allowed_depth=cur_allowed_depth, time_limit = time_remaining)

      # new_best_move, new_info = timeout(minimax,args=(current_state, use_custom_static_eval_function, use_default_move_ordering,
      #                       max_ply, info, alpha_beta, cur_allowed_depth), kwargs={}, timeout_duration=time_remaining, default=(None,None))
      if new_best_move == None:
        print("Failed with depth:"+str(cur_allowed_depth))
        break
      else:
        # print("OK")
        # print("Succeeded with depth:"+str(cur_allowed_depth))
        best_move = new_best_move
        info = new_info
        # info = info
      cur_allowed_depth += 1

      # best_move, info = minimax(current_state, use_custom_static_eval_function, use_default_move_ordering,
      #                           max_ply, info, alpha_beta, cur_allowed_depth=cur_allowed_depth)
      # n_states_expanded += temp_n_states_expanded
      # n_static_evals_performed += temp_n_static_evals_performed
      # max_depth_reached = temp_max_depth_reached
      # n_ab_cutoffs += temp_n_ab_cutoffs
      
  else:
    best_move, info = minimax(current_state, use_custom_static_eval_function, use_default_move_ordering,
                                max_ply, info, alpha_beta)


  results = []
  results.append(info["current_state_static_val"])
  results.append(info["n_states_expanded"])
  results.append(info["n_static_evals_performed"])
  results.append(info["max_depth_reached"])
  results.append(info["n_ab_cutoffs"])
  results.append(best_move)

  cur_time = time.perf_counter()
  # print("Used {} seconds".format(cur_time - start_time))
  return results

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=3,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):

  results = parameterized_minimax_helper(
       current_state,
       use_iterative_deepening_and_time,
       max_ply,
       use_default_move_ordering,
       alpha_beta, 
       time_limit,
       use_custom_static_eval_function)

  # Prepare to return the results, don't change the order of the results
  # results.append(current_state_static_val)
  # results.append(n_states_expanded)
  # results.append(n_static_evals_performed)
  # results.append(max_depth_reached)
  # results.append(n_ab_cutoffs)
  # Actually return the list of all results...
  return(results[0:5])


# def dfs(current_state, use_default_move_ordering, use_custom_static_eval_function, max_ply, cur_allowed_depth=float("inf")):
#   current_player = current_state.whose_turn

#   max_state_val, min_state_val = float("-inf"), float("inf")
#   max_state, min_state = None, None
#   visited = set()
#   stack = []
#   stack.append((current_state, 0))

#   n_states_expanded, n_static_evals_performed, max_depth_reached, n_ab_cutoffs = 0, 0, 0, 0

#   while stack:
#     state, depth = stack.pop()
#     if state in visited:
#       continue
#     elif depth > max_ply or depth > cur_allowed_depth:
#       # max_depth_reached = depth
#       continue
    
#     max_depth_reached = depth
#     n_states_expanded += 1

#     # Get state's heuristic val
#     if use_custom_static_eval_function:
#       val = state.custom_static_eval()
#     else:
#       val = state.static_eval()
    
#     n_static_evals_performed += 1

#     if val > max_state_val:
#       max_state_val = val
#       max_state = state
#     if val < min_state_val:
#       min_state_val = val
#       min_state = state


#     # Get neighbors
#     neighbors = generate_neighbors(state, current_player, use_default_move_ordering)
#     for neighbor in neighbors:
#       stack.append((neighbor, depth+1))
  
#   best_state = (min_state, max_state)
#   return n_states_expanded, n_static_evals_performed, max_depth_reached, n_ab_cutoffs, best_state

def minimax(initial_state, use_custom_static_eval_function, use_default_move_ordering,
             max_ply, info, use_alpha_beta, cur_allowed_depth=float("inf"), time_limit=float("inf"), ignore_k=False): 
  global CUR_K
  # n_states_expanded = 0
  # n_static_evals_performed = 0
  # max_depth_reached = 0
  # n_ab_cutoffs = 0
  # print("minimax")
  # print(use_custom_static_eval_function, use_default_move_ordering,
  #            max_ply, info, use_alpha_beta, cur_allowed_depth)

  import time, TTS_win_tester
  start_time = time.perf_counter()

  def minimax_helper(state, cur_depth, player,
              is_maximizer, alpha, beta, move): 
    cur_time = time.perf_counter()
    if cur_time - start_time > time_limit:
      return None, None, True
    
    # print(cur_depth, max_ply)
    if cur_depth == 0:
      if use_custom_static_eval_function:
        val = state.custom_static_eval()
      else:
        val = state.static_eval()
      info["current_state_static_val"] = val

    if cur_depth == max_ply or cur_depth == cur_allowed_depth:
      if use_custom_static_eval_function:
        val = state.custom_static_eval()
      else:
        val = state.static_eval()
      info["n_static_evals_performed"] += 1
      info["max_depth_reached"] = max(info["max_depth_reached"], cur_depth)
      return (val, None, False)
    
    if not ignore_k and move:
      if TTS_win_tester.get_win(state, move, CUR_K) != 'No win':
        if use_custom_static_eval_function:
          val = state.custom_static_eval()
        else:
          val = state.static_eval()
        return val, None, False
      
    info["n_states_expanded"] += 1
    
    if is_maximizer:
      best_move = None
      best_val = float("-inf")
      neighbors = generate_neighbors(state, player, is_maximizer, use_default_move_ordering)
      for idx, (neighbor, move) in enumerate(neighbors):
        next_player = swap_player(player)
        val, sub_move, oot = minimax_helper(neighbor, cur_depth+1, next_player, not is_maximizer, alpha, beta, move)
        if oot:
          return None, None, True
        # print(move, val)
        if val > best_val:
          best_val = val
          best_move = move
        if use_alpha_beta:
          alpha = max(alpha, best_val)
          if beta <= alpha:
            info["n_ab_cutoffs"] += (len(neighbors)-idx+1)
            break
      return (best_val, best_move, False)
    else:
      best_move = None
      best_val = float("inf")
      neighbors = generate_neighbors(state, player, is_maximizer, use_default_move_ordering)
      for idx, (neighbor, move) in enumerate(neighbors):
        next_player = swap_player(player)
        val, sub_move, oot = minimax_helper(neighbor, cur_depth+1, next_player, not is_maximizer, alpha, beta, move)
        if oot:
          return None, None, True
        if val < best_val:
          best_val = val
          best_move = move
        if use_alpha_beta:
          beta = min(beta, best_val)
          if beta <= alpha:
            info["n_ab_cutoffs"] += (len(neighbors)-idx+1)
            break
      return (best_val, best_move, False)
  
  player = initial_state.whose_turn
  # print(player)
  if player == "W":
    player_is_maximizer = True # Use player to determine
  else:
    player_is_maximizer = False
  best_val, best_move, oot = minimax_helper(initial_state, 0, player, player_is_maximizer, float("-inf"), float("inf"), None)
  # print("Best move:",(best_move))
  if oot:
    return None, None
  else:
    return best_move, info

def swap_player(player):
  if player == "W":
    return "B"
  else:
    return "W"
  
def generate_neighbors(state, player, is_max, use_default_move_ordering):
  neighbors = []
  if use_default_move_ordering or not use_default_move_ordering:
    # Generate neighbors top left, to top right, then downwards
    for row_idx in range(len(state.board)):
      for col_idx in range(len(state.board[0])):
        # Only move to the section if it is open
        if state.board[row_idx][col_idx] == ' ':
          state_copy = MY_TTS_State(state.board, whose_turn=player)
          state_copy.board[row_idx][col_idx] = player
          neighbors.append((state_copy, (row_idx, col_idx)))
    # print(neighbors)
    return neighbors
  else:
    for row_idx in range(len(state.board)):
      for col_idx in range(len(state.board[0])):
        # Only move to the section if it is open
        if state.board[row_idx][col_idx] == ' ':
          state_copy = MY_TTS_State(state.board, whose_turn=player)
          state_copy.board[row_idx][col_idx] = player
          # Check val for state
          val = state_copy.custom_static_eval()
          neighbors.append((state_copy, (row_idx, col_idx), val))
    if is_max:
      neighbors.sort(key=lambda x: x[2], reverse=True)
    else:
      neighbors.sort(key=lambda x: x[2], reverse=False)

    return [(neighbor[0], neighbor[1]) for neighbor in neighbors]
      
      
# Testing

INITIAL_BOARD = \
               [['-','B',' ','-',' ',' ','-'],
                [' ',' ',' ','W',' ',' ',' '],
                [' ','B',' ',' ',' ',' ',' '],
                ['-',' ',' ','-',' ',' ','-'],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                ['-',' ',' ','-',' ',' ','-']]
state = MY_TTS_State(INITIAL_BOARD)
# val = state.static_eval()

val = state.custom_static_eval()
print(val)

# print(state)
# print(state)

# res = parameterized_minimax_helper(
#        current_state=state,
#        use_iterative_deepening_and_time = False,
#        max_ply=3,
#        use_default_move_ordering = True,
#        alpha_beta=False, 
#        time_limit=1.0,
#        use_custom_static_eval_function=True)
# print(res[-1])

# res = parameterized_minimax_helper(
#        current_state=state,
#        use_iterative_deepening_and_time = False,
#        max_ply=4,
#        use_default_move_ordering = True,
#        alpha_beta=True, 
#        time_limit=1.0,
#        use_custom_static_eval_function=True)
# print(res[-1])
# print("current_state_static_val", res[0])
# print("n_states_expanded", res[1])
# print("n_static_evals_performed", res[2])
# print("max_depth_reached", res[3])
# print("n_ab_cutoffs", res[4])