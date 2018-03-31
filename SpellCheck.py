from __future__ import division
import pandas as pd
import re
from collections import Counter


spell_check_error = pd.read_csv('/Users/durveshvedak/Documents/Spring 2018/Into to DS/Spell Check Model/spell-errors.txt')
test = pd.read_csv('/Users/durveshvedak/Documents/Spring 2018/Into to DS/Spell Check Model/test.csv',header=0)
countOfWords = pd.read_csv('/Users/durveshvedak/Documents/Spring 2018/Into to DS/Spell Check Model/count_1w.txt', sep="\t", header=None)
countOfWords=countOfWords.rename(index=str,columns={0:"Word",1:"Count"})
TEXT = open('/Users/durveshvedak/Documents/Spring 2018/Into to DS/Spell Check Model/big.txt').read()

def tokens(TEXT):
    return re.findall('[a-z]+',TEXT.lower())

WORDS = tokens(TEXT)
COUNTS = Counter(WORDS)
print(COUNTS.most_common(10))

def known(words):
    #Return the subset of words that are actually in the dictionary."
    return {w for w in words if w in COUNTS}

def edits0(word):
    return {word}

def edits2(word):
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def edits1(word):
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def splits(word):
    return [(word[:i], word[i:])
            for i in range(len(word)+1)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def correct(word):
    #Generating all the words with edit distance of 0, 1 & 2
    candidates = (known(edits0(word)) or
                  known(edits1(word)) or
                  known(edits2(word)) or
                  [word])
    return max(candidates, key=COUNTS.get)

def correct_text(text):
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    word = match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)

for w in test.WRONG:
    print(correct_text(w))





