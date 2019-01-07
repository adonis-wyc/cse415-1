def five_x_cubed_plus_1(n):
    return 5 * (n ** 3) + 1

def pair_off(n):
    pairs = []
    for x in range(int (len(n) / 2)):
        pairs.append([n[x * 2], n[x * 2 + 1]])
    if (int (len(n) % 2) == 1):
        pairs.append([n[-1]])
    return pairs

def mystery_code(n):
    return "hi"


print(pair_off([1, 2, 3, 4, 5, 'a', 'b', ['x', 'y'], ['z'], 'second from last', 'last']))