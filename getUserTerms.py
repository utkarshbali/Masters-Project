import pickle
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import datetime

userTweets = {}
userTerms = {}

def tokenizeTweets():
    global userTerms
    tknzr = TweetTokenizer(preserve_case = False)
    for user in userTweets:
        tweetInfo = userTweets[user]
        for tweet in tweetInfo:
            timeStamp = tweetInfo[tweet][1]
            convTimeStamp = datetime.datetime.strptime(timeStamp,'%a, %d %b %Y %H:%M:%S +0000')
            tweetCount = tweetInfo[tweet][0]
            words = tknzr.tokenize(tweet)
            for word in words:
                count = tweetCount
                terms = userTerms.get(user,{})
                if not isStopWord(word):
                    if (word in terms):
                        count = terms[word][0] + count
                        timeTerms = terms[word][1]
                        convTime = datetime.datetime.strptime(timeTerms,'%a, %d %b %Y %H:%M:%S +0000')
                        if (convTime>convTimeStamp):
                            timeStamp = timeStamp
                        else:
                            timeStamp = timeTerms
                    terms[word] = [count,timeStamp]
                    userTerms[user] = terms
        
def isStopWord(word):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']#,'"','.'
    if word in stop:
        return True
    else:
        return False
            
def getUserTweets():
    global userTweets
    userTweets = pickle.load(open("userTweets.pkl","rb"))

def main():
    getUserTweets()    
    tokenizeTweets()
    pickle.dump(userTerms,open("userTerms.pkl","wb"))
    
        #term = nltk.word_tokenize(tweet.encode('ascii', 'ignore'))
    
if __name__ == "__main__":
    main()