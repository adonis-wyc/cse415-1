F = 'front'
B = 'back'
U = 'upper'
D = 'down'
L = 'left'
R = 'right'

OPPOSITE = {F:B,
            B:F,
            U:D,
            D:U,
            L:R,
            R:L}

# Left, right, up, down face with respect to one side
# Left, down, right, up
ADJACENT = {F: [L,D,R,U],
            B: [R,D,L,U],
            U: [L,F,R,B],
            D: [L,B,R,F],
            L: [B,D,F,U],
            R: [F,D,B,U]}

GOAL = {F: ['blue', 'blue','blue', 'blue'],
        B: ['green', 'green','green', 'green'],
        U: ['white', 'white','white', 'white'],
        D: ['yellow', 'yellow','yellow', 'yellow'],
        L: ['red', 'red','red', 'red'],
        R: ['orange', 'orange','orange', 'orange']}


class State:
    def __init__(self, s):
        self.b = s
    
    def __eq__(self, s2):
        for key in self.b:
            for i in range(4):
                if self.b[key][i] != s2.b[key][i]:
                    return False
        return True
    
    def __str__(self):
        txt = 'Left:\n[' + self.b[L][0] + ', ' + self.b[L][1] + '\n' + self.b[L][2] + ', ' + self.b[L][3]
        # for i in range(1,4):
        #     txt += ', ' + self.b[L][i]
        return txt + ']'
    
    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        news = State({})
        news.b = {key: value[:] for key, value in self.b.items()}
        return news
    
    def can_move(self, dir):
        return True
    
    def move(self, dir):
        news = self.copy()
        face = news.b[dir]
        temp = face[0]
        face[0] = face[2]
        face[2] = face[3]
        face[3] = face[1]
        face[1] = temp
        news.b[dir] = face

        adj = ADJACENT[dir]
        # Second and fourth tile on left face
        c1 = news.b[adj[0]][1]
        c2 = news.b[adj[0]][3]

        # Swap tiles
        news.b[adj[0]][1] = news.b[adj[1]][0]
        news.b[adj[0]][3] = news.b[adj[1]][1]
        news.b[adj[1]][0] = news.b[adj[2]][2]
        news.b[adj[1]][1] = news.b[adj[2]][0]
        news.b[adj[2]][2] = news.b[adj[3]][3]
        news.b[adj[2]][0] = news.b[adj[3]][2]
        news.b[adj[3]][3] = c1
        news.b[adj[3]][2] = c2

        return news
    
    def edge_distance(self, s2):
        return 1.0
    
def goal_test(s):
    return s.b == GOAL
    
def goal_message(s):
    return "You done it!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# initial_state = {F: ['blue', 'blue','blue', 'blue'],
#                 B: ['green', 'green','green', 'green'],
#                 U: ['white', 'white','red', 'red'],
#                 D: ['orange', 'orange','yellow', 'yellow'],
#                 L: ['red', 'yellow','red', 'yellow'],
#                 R: ['white', 'orange','white', 'orange']}

Z = 'blue'
Y = 'yellow'
G = 'green'
W = 'white'
O = 'orange'
X = 'red'

initial_state = {F: [O,O,O,O],
                B: [R,R,R,R],
                U: [G,G,W,W],
                D: [Y,Y,Z,Z],
                L: [W,Z,W,Z],
                R: [G,Y,G,Y]}
CREATE_INITIAL_STATE = lambda: State(initial_state)

directions = [F, B, U, D, L, R]
OPERATORS = [Operator("Rotate " +str(dir)+ " clockwise",
                lambda s,dir1=dir: s.can_move(dir1),
                lambda s,dir1=dir: s.move(dir1) )
            for dir in directions]

GOAL_TEST = lambda s: goal_test(s)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)