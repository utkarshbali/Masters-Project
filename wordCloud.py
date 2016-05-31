from wordcloud import WordCloud
import pickle
import matplotlib.pyplot as plt
#from scipy.misc import imread

wordGraph = pickle.load(open("wordGraph_200.pkl","rb"))
wordGraph2 = pickle.load(open("wordGraph_500.pkl","rb"))
wordGraph3 = pickle.load(open("wordGraph_750.pkl","rb"))

text = " "

for graph in wordGraph:
    word = graph
    text = text + word +" "
for graph in wordGraph2:
    word = graph
    text = text + word +" "
    
for graph in wordGraph3:
    word = graph
    text = text + word +" "    
    
#alice_mask = imread("img.tiff")
wc = WordCloud(max_words=2000,max_font_size=40, relative_scaling=.5)
wordcloud = wc.generate(text)
# Open a plot of the generated image.
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('wc_rect.eps', format='eps', dpi=1500)
plt.show()# -*- coding: utf-8 -*-

