from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

k = 0
my_side = 'B'

BLACK = "B"
WHITE = "W"
opponent = {
            "B": "W",
            "W": "B"
            }

class MY_TTS_State(TTS_State):
    def static_eval(self, color):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else :
            return self.basic_static_eval(color)

    def basic_static_eval(self, color):
        value = 0
        other_color = opponent[color]
        x = len(self.board[0])
        y = len(self.board)
        # Check all horizontal lines
        for row in self.board:
            pieces = 0
            blocked = False
            for tile in row:
                if tile == '-' or tile == other_color:
                    blocked = True
                    break
                if tile == color:
                    pieces += 1
            if blocked:
                continue
            if pieces == 2:
                #print('horizontal value: ' + str(value))
                value += 1
        
        # Check all vertical lines
        for i in range(x):
            pieces = 0
            blocked = False
            for j in range(y):
                tile = self.board[j][i]
                if tile == '-' or tile == other_color:
                    blocked = True
                    break 
                if tile == color:
                    pieces += 1
            if blocked:
                continue
            if pieces == 2:
                #print('vertical value: ' + str(value))
                value += 1
        
        # If board dimension isn't divisible (larger side / smaller side),
        # diagonal count will be the entire board.
        if (x > y and x % y != 0) or (x < y and y % x != 0):
            pieces = 0
            for row in self.board:
                for tile in row:
                    if tile == '-' or tile == other_color:
                        return value
                    elif tile == color:
                        pieces += 1
            if pieces == 2:
                value += 2
            return value
        
        # Diagnoal to the right
        if x >= y:
            for i in range(y):
                pieces = 0
                blocked = False 
                for j in range(x): 
                    tile = self.board[(j + i) % y][j]
                    if tile == '-' or tile == other_color:
                        blocked = True 
                        break 
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    #print('rd1 value: ' + str(value))
                    value += 1
        else:
            for i in range(x):
                pieces = 0
                blocked = False 
                for j in range(y): 
                    tile = self.board[j][(j + i) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True 
                        break 
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    #print('rd2 value: ' + str(value))
                    value += 1

        # Diagonal to the left
        if x >= y:
            for i in range(y):
                pieces = 0
                blocked = False 
                for j in range(x): 
                    tile = self.board[j % y][(x + i - j) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True 
                        break 
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    #print('ld1 value: ' + str(value))
                    value += 1
        else:
            for i in range(x):
                pieces = 0
                blocked = False 
                for j in range(y): 
                    tile = self.board[j][(y + i - j) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True 
                        break 
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    #print('ld2 value: ' + str(value))
                    value += 1

        return value

    def custom_static_eval(self):
        raise Exception("custom_static_eval not yet implemented.")
    
    def get_ordered_moves(self, color):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] == ' '):
                    new_state = MY_TTS_State(self.board)
                    new_state.board[i][j] = color
                    moves.append(new_state)
        return moves


def get_ready(initial_state, _k, what_side_i_play, opponent_moniker):
    global k, my_side
    k = _k
    my_side = what_side_i_play
    return 1

def who_am_i():
    return 'I am me'

def moniker():
    return 'Shrek'

def take_turn(current_state, opponents_utterance, time_limit = 10):
    return 'Ok'

eval_value = 0
states_expanded = 0
states_evaluated = 0
maximum_depth = 0
num_cutoff = 0
time = 0

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):
    global USE_CUSTOM_STATIC_EVAL_FUNCTION, eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, time
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    new_state = MY_TTS_State(current_state.board)

    best_state = ''
    if not alpha_beta:
        best_state = minimax_search(1, max_ply, new_state, BLACK)
    return [eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff]

def minimax_search(current_depth, max_ply, current_state, color):
    global eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, time, my_side
    if current_depth > maximum_depth:
        maximum_depth = current_depth

    new_state = MY_TTS_State(current_state.board)
    moves = new_state.get_ordered_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        states_expanded += 1
        return current_state
    
    eval_value = 0
    if current_depth % 2 == 1:
        eval_value = float("-inf")
    else:
        eval_value = float("inf")
    optimal_state = ''
    for move in moves:
        states_expanded += 1
        state = minimax_search(current_depth + 1, max_ply, move, opponent[my_side])
        move_value = state.static_eval(my_side) - state.static_eval(opponent[my_side])
        if current_depth % 2 == 1 and move_value > eval_value:
            optimal_state = move
            eval_value = move_value
        if current_depth % 2 == 0 and move_value < eval_value:
            optimal_state = move
            eval_value = move_value
    
    return optimal_state

def minimax_pruning(current_depth, max_ply, current_state, color, alpha, beta):
    global eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, time, my_side
    if current_depth > maximum_depth:
        maximum_depth = current_depth
    
    new_state = MY_TTS_State(current_state.board)
    moves = new_state.get_ordered_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        states_expanded += 1
        return current_state

    for move in moves:
        states_expanded += 1
    return 1

INITIAL_BOARD = \
                [[' ',' ',' ',' '],
                [' ',' ','B',' '],
                [' ','B','B',' '],
                [' ','B',' ','B']]

# INITIAL_BOARD = \
#                 [['B',' '],
#                 ['B',' '],
#                 [' ','B'],
#                 [' ','B']]

# INITIAL_BOARD = \
#                 [['B',' ','B','B',' ',' ',' ',' ',' '],
#                 [' ',' ',' ',' ',' ',' ',' ',' ',' '],
#                 [' ',' ',' ',' ','-',' ',' ',' ','B']]

init_state = TTS_State(INITIAL_BOARD)
new_state = MY_TTS_State(init_state.board)
result = parameterized_minimax(new_state, False, 2, True, False, 1.0, False)
for i in result:
    print(str(i))