import pickle
from nltk.tokenize import TweetTokenizer
import re
import json

def readPickle(filename):
    return pickle.load(open(filename,"rb"))

def main():
    rocWords = readPickle("Independent/rocWords.pkl")
    nycWords = readPickle("Independent/nycWords.pkl")
    vegasWords = readPickle("Independent/lasVegasWords.pkl")
    detroitWords = readPickle("Independent/detroitWords.pkl")
    vocab = {}
    for word in rocWords:
        vocab[word] = rocWords[word]
    for word in nycWords:
        if word in vocab:
            vocab[word] = nycWords[word] + vocab[word]
        else:
            vocab[word] = nycWords[word]
    for word in vegasWords:
        if word in vocab:
            vocab[word] = vegasWords[word] + vocab[word]
        else:
            vocab[word] = vegasWords[word]
    for word in detroitWords:
        if word in vocab:
            vocab[word] = detroitWords[word] + vocab[word]
        else:
            vocab[word] = detroitWords[word]
            
    pickle.dump(vocab,open("Independent/vocab.pkl","wb"))