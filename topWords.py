import pickle
import operator

userTerms = {}
terms = {}
words = {}
sortedWords = {}
def getUserTerms():
    global userTerms
    userTerms = pickle.load(open("userTerms.pkl","rb"))

def main():
    global terms,words,sortedWords
    getUserTerms()
    #UDG = DG.to_undirected(reciprocal = True)
    #nx.draw(UDG)
    for userId in userTerms:
        terms = userTerms[userId]
        for term in terms:
            #timeStamp = terms[term][1]
            termCount = terms[term][0]
            if term in words:
               termCount = words[term] + termCount
            else:
               termCount = terms[term][0]
            words[term] = termCount
    sortedWords = sorted(words.items(), key=operator.itemgetter(1),reverse = True)    
    pickle.dump(sortedWords,open('topWords.pkl','wb'))


if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-