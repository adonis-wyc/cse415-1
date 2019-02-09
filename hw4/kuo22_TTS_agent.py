from TTS_State import TTS_State
import time

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

k = 5
my_side = 'W'

BLACK = "B"
WHITE = "W"
opponent = {
            "B": "W",
            "W": "B"
            }

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else :
            return self.basic_static_eval(WHITE) - self.basic_static_eval(BLACK)

    def basic_static_eval(self, color):
        global k
        value = 0
        other_color = opponent[color]
        x = len(self.board[0])
        y = len(self.board)

        # Check all horizontal lines
        # if k == x:
        #     for row in self.board:
        #         pieces = 0
        #         blocked = False
        #         for tile in row:
        #             if tile == '-' or tile == other_color:
        #                 blocked = True
        #                 break
        #             if tile == color:
        #                 pieces += 1
        #         if blocked:
        #             continue
        #         if pieces == 2:
        #             value += 1
        # elif k < x:
        for row in self.board:
            for i in range(x):
                pieces = 0
                blocked = False
                for j in range(k):
                    tile = row[(i + j) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
        # print('horizontal ' + str(value))
        # Check all vertical lines
        # if k == y:
        #     for i in range(x):
        #         pieces = 0
        #         blocked = False
        #         for j in range(y):
        #             tile = self.board[j][i]
        #             if tile == '-' or tile == other_color:
        #                 blocked = True
        #                 break 
        #             if tile == color:
        #                 pieces += 1
        #         if blocked:
        #             continue
        #         if pieces == 2:
        #             #print('vertical value: ' + str(value))
        #             value += 1
        # elif k < y:
        for i in range(x):
            for j in range(y):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(j + t) % y][i]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
        
        # print('vertical ' + str(value))

        # If board dimension isn't divisible (larger side / smaller side),
        # diagonal count will be the entire board.
        if (x > y and x % y != 0) or (x < y and y % x != 0):
            if k == x*y:
                for row in self.board:
                    for tile in row:
                        if tile != color:
                            return value
                # All tiles are the target color, so diagonal in both directions count
                value += 2 
                return value
        
        # For squares or rectangles with length 2 on one side (that have divisible dimensions),
        # the diagonal lines are cyclic if k = max length, so only need to 
        # check for lines with starting point on the top row.
        # if k == max(x, y) and (x == y or (x == 2 or y == 2)):
        #     # if x >= y:
        #     # Down-right diagonal
        #     for i in range(x):
        #         pieces = 0
        #         blocked = False
        #         for j in range(y):
        #             tile = self.board[j % y][(i + j) % x]
        #             if tile == '-' or tile == other_color:
        #                 blocked = True
        #                 break
        #             if tile == color:
        #                 pieces += 1
        #         if blocked:
        #             continue
        #         if pieces == 2:
        #             value += 1
        #     # print('down-right ' + str(value))

        #     # Down-left diagonal
        #     for i in range(x):
        #         pieces = 0
        #         blocked = False
        #         for j in range(y):
        #             tile = self.board[j % y][(i - j) % x]
        #             if tile == '-' or tile == other_color:
        #                 blocked = True
        #                 break
        #             if tile == color:
        #                 pieces += 1
        #         if blocked:
        #             continue
        #         if pieces == 2:
        #             value += 1
        #     # print('down-left ' + str(value))

        # elif k < x*y:
        # Check for diagonals going down-right
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j + t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1

        # print('down-right ' + str(value))
        # Check for diagonals going down-left
        for i in range(y):
            for j in range(x):
                pieces = 0
                blocked = False
                for t in range(k):
                    tile = self.board[(i + t) % y][(j - t) % x]
                    if tile == '-' or tile == other_color:
                        blocked = True
                        break
                    if tile == color:
                        pieces += 1
                if blocked:
                    continue
                if pieces == 2:
                    value += 1
            # print('down-left ' + str(value))
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
    global start_time, time_lim, my_side
    start_time = time.perf_counter()
    time_lim = time_limit
    new_state = MY_TTS_State(current_state.board)
    best_state = None

    current_max_ply = 1
    while current_max_ply <= 10:
        best_state = best_move(0, current_max_ply, new_state, my_side, float("-inf"), float("inf"))
        current_max_ply += 1
        end_time = time.perf_counter()
        if end_time - start_time > time_limit * 0.9:
            break   
    x = 0
    y = 0
    moved = False
    for i in range(len(new_state.board)):
        for j in range(len(new_state.board[0])):
            if new_state.board[i][j] != best_state.board[i][j]:
                x = j
                y = i
                moved = True
                break
        if moved:
            break
    
    if not moved:
        return [[False, current_state], "I can't move, dummy!"]
    else:
        return [[(y,x), best_state], "Look at this awesome move!"]


# Best search for my agent. Modification of alpha-beta pruning with less overhead
def best_move(current_depth, max_ply, current_state, color, alpha, beta):
    global my_side, start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.9:
        return current_state

    moves = current_state.get_ordered_moves(color)
    if not moves or current_depth == max_ply:
        return current_state

    optimal_state = current_state
    for move in moves:
        state = minimax_pruning(current_depth + 1, max_ply, move, opponent[my_side], alpha, beta)
        move_value = state.static_eval()
        if color == WHITE:
            if move_value > alpha:
                alpha = move_value
                optimal_state = move
        else:
            if move_value < beta:
                beta = move_value
                optimal_state = move
        
        # Prune step
        if alpha >= beta:
            return optimal_state

    return optimal_state


eval_value = 0
states_expanded = 0
states_evaluated = 0
maximum_depth = 0
num_cutoff = 0
start_time = 0
time_lim = 0

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False, 
       time_limit=1.0,
       use_custom_static_eval_function=False):

    global USE_CUSTOM_STATIC_EVAL_FUNCTION, eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, start_time, time_lim

    start_time = time.perf_counter()
    time_lim = time_limit
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    new_state = MY_TTS_State(current_state.board)
    best_state = None

    if alpha_beta:
        if use_iterative_deepening_and_time:
            current_max_ply = 1
            while current_max_ply <= max_ply:
                best_state = minimax_pruning(0, current_max_ply, new_state, my_side, float("-inf"), float("inf"))
                current_max_ply += 1
                end_time = time.perf_counter()
                if end_time - start_time > time_limit * 0.9:
                    break
        else:
            best_state = minimax_pruning(0, max_ply, new_state, my_side, float("-inf"), float("inf"))
    else:
        if use_iterative_deepening_and_time:
            current_max_ply = 1
            while current_max_ply <= max_ply:
                best_state = minimax_search(0, current_max_ply, new_state, my_side)
                current_max_ply += 1
                end_time = time.perf_counter()
                if end_time - start_time > time_limit * 0.9:
                    break   
        else:
            best_state = minimax_search(0, max_ply, new_state, my_side)
    eval_value = best_state.static_eval()
    print(str(best_state))
    end_time = time.perf_counter()
    print("time: " + str(end_time - start_time))
    return [eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff]

def minimax_search(current_depth, max_ply, current_state, color):
    global eval_value, states_expanded, states_evaluated, maximum_depth, num_cutoff, my_side, start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.9:
        return current_state

    if current_depth > maximum_depth:
        maximum_depth = current_depth

    # new_state = MY_TTS_State(current_state.board)
    moves = current_state.get_ordered_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        states_expanded += 1
        return current_state
    
    optimal_value = 0
    if color == WHITE:
        optimal_value = float("-inf")
    else:
        optimal_value = float("inf")
    optimal_state = None
    for move in moves:
        states_expanded += 1
        state = minimax_search(current_depth + 1, max_ply, move, opponent[my_side])
        move_value = state.static_eval()
        if color == WHITE and move_value > optimal_value:
            optimal_state = move
            optimal_value = move_value
        if color == BLACK and move_value < optimal_value:
            optimal_state = move
            optimal_value = move_value
    return optimal_state

# Minimax with alpha-beta pruning
def minimax_pruning(current_depth, max_ply, current_state, color, alpha, beta):
    global states_expanded, states_evaluated, maximum_depth, num_cutoff, time, my_side, start_time, time_lim

    current_time = time.perf_counter()
    if current_time - start_time > time_lim * 0.9:
        return current_state

    if current_depth > maximum_depth:
        maximum_depth = current_depth
    
    moves = current_state.get_ordered_moves(color)
    if not moves or current_depth == max_ply:
        states_evaluated += 1
        states_expanded += 1
        return current_state


    optimal_state = current_state
    for move in moves:
        states_expanded += 1
        state = minimax_pruning(current_depth + 1, max_ply, move, opponent[my_side], alpha, beta)
        move_value = state.static_eval()
        if color == WHITE:
            if move_value > alpha:
                alpha = move_value
                optimal_state = move
        else:
            if move_value < beta:
                beta = move_value
                optimal_state = move
        
        # Prune step
        if alpha >= beta:
            num_cutoff += 1
            return optimal_state

    return optimal_state

# INITIAL_BOARD = \
#                 [[' ',' ',' ',' '],
#                 [' ','B',' ',' '],
#                 [' ',' ','B',' '],
#                 [' ',' ',' ',' ']]

# INITIAL_BOARD = \
#                 [[' ',' ',' ','W','B'],
#                 ['-','B',' ',' ',' '],
#                 [' ',' ','B',' ',' '],
#                 [' ',' ',' ','W',' ']]

INITIAL_BOARD = \
                [['W','W'],
                [' ',' '],
                [' ',' '],
                [' ',' ']]

# INITIAL_BOARD = \
#                 [[' ',' ','W',' ',' ',' ',' ',' ',' '],
#                 ['B',' ','B','B',' ',' ',' ',' ',' '],
#                 [' ',' ',' ',' ','-',' ',' ',' ','B']]

init_state = TTS_State(INITIAL_BOARD)
new_state = MY_TTS_State(init_state.board)
print(new_state.static_eval())
# result = parameterized_minimax(new_state, True, 6, True, False, 5.0, False)
# for i in result:
#     print(str(i))