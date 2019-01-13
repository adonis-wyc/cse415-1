from random import choice
from re import *

def introduce():
    return """I am Shrek.
        I am a mean green ogre. You better stop bothering me before I send you to my belly.
        Don't try to say anything that will make me angry.
        Kuo Hong made me.
        If you got a problem, go bother him at kuo22@uw.edu."""

def agentName():
    return 'Shrek'

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")    

asked = False
gender = ''
math = False

def respond(the_input):
    wordlist = split(' ',remove_punctuation(the_input))
    wordlist[0]=wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0]=mapped_wordlist[0].capitalize()

    global asked
    global gender
    global math

    # Asks others to same something if input is empty
    if wordlist[0] == '':
        return "Don't just stare at me.  Say something!"
    # Gives the location of home when asked "where do you live"
    if wordlist[0:4] == ['where', 'do', 'you', 'live']:
        return "I live in a beautiful swamp where I enjoy every day of my life."
    # Returns randomly generated feeling when asked "how are you"
    if wordlist[0:3] == ['how', 'are', 'you']:
        feeling = choice(['happy', 'sad', 'angry', 'mad', 'anxious', 'content'])
        return "I feel " + feeling + " right now."
    # Returns an encouraging agreement to responses that start with "I will"
    if wordlist[0:2] == ['i', 'will'] and len(wordlist) > 2:
        return "Interesting.  I hope you " + stringify(mapped_wordlist[2:]) + " too."
    # Returns aggressive response when asked where something is
    if wordlist[0:2] == ['where', 'is']:
        return "What makes you think I know?  Go find it yourself."
    # Returns the next verse after "Shrek is love"
    if wordlist[0:3] == ['shrek', 'is', 'love']:
        return "Shrek is life."
    # Returns a mean remark when the response contains "bored"
    if 'bored' in wordlist:
        return "Why don't you get outta here and find something to do."
    # Returns annoyed comment when response mentions "donkey"
    if 'donkey' in wordlist:
        return "Oh, don't remind me of that guy again."
    # Remembers the gender of the other agent if response mentions "boy" and the question "are you a boy or a girl" has been asked
    if 'boy' in wordlist and asked == True and gender == '':
        gender = 'boy'
        return "Okay, I will remember that."
    # Remembers the gender of the other agent if response mentions "girl" and the question "are you a boy or a girl" has been asked
    if 'girl' in wordlist and asked == True and gender == '':
        gender = 'girl'
        return "Okay, I will remember that."
    # Returns a prideful remark when response mentions "swamp"
    if 'swamp' in wordlist:
        return "Yes, my swamp is very beautiful."
    # Returns a retaliation when response mentions "fear"
    if 'fear' in wordlist:
        return "I ain't afraid of you!"
    # Sings a verse from the song All Star when certain music keywords are mentioned
    for word in ['star', 'sing', 'song']:
        if word in wordlist:
            return sing()
    # Returns a depressing reply if "princess" or "fiona" is mentioned
    for word in ['princess', 'fiona']:
        if word in wordlist:
            return "Oh, I miss her. Things have not been the same ever since she left me."
    # Compatible with my partner's agent. Asks other agent to stop talking about math if the response contains certain math terms.
    for word in ['graph', 'vertices', 'epsilon', 'topology']:
        if word in wordlist:
            if not math:
                math = True
                return "Stop talking about math, I don't know what you mean."
            else:
                return choice(["Stop with your nerdy nonsense! Leave today or I will cook you for dinner.", "I am really mad now!"])
    # Returns an annoyed comment if response starts with a questioning word.
    if wpred(wordlist[0]):
        return "I am not an encyclopedia.  Stop bothering me!"
    # Starts by asking if other agent is a boy or a girl. Then cycles through various insults if no other rules trigger.
    else:
        if (asked == False):
            asked = True
            return "So are you a boy or a girl?"
        if (gender == ''):
            return other() + "."
        else:
            return other() + choice([", little " + gender, '']) + "."

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

LYRIC = ['Somebody once told me the world is gonna roll me', "I ain't the sharpest tool in the shed", "She was looking kind of dumb with her finger and her thumb", 'In the shape of an "L" on her forehead']

OTHER = ['I have no idea what you are talking about', 'Stop speaking gibberish', 'I will knock you out', "I ain't got all day", 'Speak up! Do you fear me']

count = 0
# Cycles through a few insults
def other():
    global count
    count += 1
    return OTHER[count % 5]

lyric_count = -1
# Cycles through the first few lines of All Star
def sing():
    global lyric_count
    lyric_count += 1
    return LYRIC[lyric_count % 4]