from random import choice
from re import *


def introduce():
    return """I am Shrek the ogre.
        Kuo Hong made me.
        If you got a problem, go bother him at kuo22@uw.edu."""

def agentName():
    return 'Shrek'

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")    

EMOTIONS = {
    1: 'happy',
    2: 'sad',
    3: 'angry',
    4: 'mad',
    5: 'anxious',
    6: 'content'
}

def respond(the_input):
    wordlist = split(' ',remove_punctuation(the_input))
    wordlist[0]=wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0]=mapped_wordlist[0].capitalize()

    if wordlist[0] == '':
        return "Don't just stare at me.  Say something!"
    if wordlist[0:4] == ['where', 'do', 'you', 'live']:
        return "I live in a beautiful swamp where I enjoy every day of my life."
    if wordlist[0:3] == ['how', 'are', 'you']:
        feeling = choice(['happy', 'sad', 'angry', 'mad', 'anxious', 'content'])
        return "I feel " + feeling + " right now."
    if wordlist[0:2] == ['i', 'will']:
        return "Cool!  I hope you " + stringify(mapped_wordlist[2:]) + "."
    if 'bored' in wordlist:
        return "Why don't you get outta here and find something to do."
    else:
        return 'sup'

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