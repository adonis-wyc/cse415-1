from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

k = 0
my_side = ''

BLACK = "B"
WHITE = "W"
opponent = {
            "B": "W",
            "W": "B"
            }

class MY_TTS_State(TTS_State):
    def static_eval(self, color, n):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else :
            return self.basic_static_eval(color, n)

    def basic_static_eval(self, color, n):
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
                print('horizontal value: ' + str(value))
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
                print('vertical value: ' + str(value))
                value += 1
        
        if (x > y and x % y != 0) or (x < y and y % x != 0):
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
                    print('rd1 value: ' + str(value))
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
                    print('rd2 value: ' + str(value))
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
                    print('ld1 value: ' + str(value))
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
                    print('ld2 value: ' + str(value))
                    value += 1

        return value

    def custom_static_eval(self):
        raise Exception("custom_static_eval not yet implemented.")

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

def minimax_search(level):
    return 1

def parameterized_minimax( ** keywordargs):
    return 'Cool'

# INITIAL_BOARD = \
#                 [[' ',' ',' ',' '],
#                 [' ',' ','B',' '],
#                 [' ','B','B',' '],
#                 [' ','B',' ','B']]

# INITIAL_BOARD = \
#                 [['B',' '],
#                 ['B',' '],
#                 [' ','B'],
#                 [' ','B']]

INITIAL_BOARD = \
                [['B',' ','B','B',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ','-',' ',' ',' ','B']]

init_state = TTS_State(INITIAL_BOARD)
new_state = MY_TTS_State(init_state.board)
print(new_state.static_eval('B', 2))