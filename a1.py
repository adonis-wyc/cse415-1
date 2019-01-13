irregular = {
    'have': 'had',
    'be': 'was',
    'am': 'was',
    'is': 'was',
    'are': 'were',
    'eat': 'ate',
    'go': 'went'
}

# Returns 5 * n^3 + 1
def five_x_cubed_plus_1(n):
    return 5 * (n ** 3) + 1

# Takes a list n and returns another list containing lists each containing two consecutive elements from n.
# Last pair only contains one element if n has odd number of elements.
def pair_off(n):
    pairs = []
    for x in range(int (len(n) / 2)):
        pairs.append([n[x * 2], n[x * 2 + 1]])
    if (int (len(n) % 2) == 1):
        pairs.append([n[-1]])
    return pairs

# Changes input string by shifting alphabets 19 places up and change its case.
def mystery_code(n):
    output = ''
    for c in n:
        char = c
        if c.isalpha():
            if c.upper() <= 'G':
                if c.islower():
                    char = chr(ord(c.upper()) + 19).upper()
                else:
                    char = chr(ord(c) + 19).lower()
            else:
                if c.islower():
                    char = chr(ord(c.upper()) - 7).upper()
                else:
                    char = chr(ord(c) - 7).lower()
        output += char
    return output

# Takes a verb base form and returns the past tense of that verb
def past_tense(n):
    verbs = []
    for verb in n:
        verbs.append(irregular.get(verb, other_verbs(verb)))
    return verbs

def other_verbs(n):
    if (len(n) > 2):
        if n[-1] == 'e':
            return n + 'd'
        elif n[-1] == 'y' and n[-2] not in 'aeiou':
            return n[:-1] + 'ied'
        elif n[-1] not in 'aeiouyw' and n[-2] in 'aeiou' and n[-3] not in 'aeiou':
            return n + n[-1] + 'ed'
        else:
            return n + 'ed'