#!/usr/bin/env python2.7


""" @package default
[USAGE]
python wordcount.py | tee debug.txt

More details..
"""

import operator
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.collocations import *


txtfile = open('topic/all_topics.txt', 'r+')
filepath = os.path.abspath(txtfile.name)
wordcount = {}
wnl = WordNetLemmatizer()
# Collect no-meaning words.
stop = stopwords.words('english')
# (TODO) Should seperate by '\n'..
words = [w.translate(None, ',.?-()_\"').lower() for w in txtfile.read().split()]

stemmed_words = []
for word in words:
    # (??) Two times 'not in stop' 
    # if word not in stop:
    # stemmed_word = stem(wnl.lemmatize(word))

    # stemmed_word = wnl.lemmatize(word)

    # the parameter of 'lemmatize()' need to be Unicode, or it will
    # transform the Ascii String to Unicode at the very beginning
    # using default Ascii Decoder. Therefore, generate 'UnicodeDecodeError'
    stemmed_word = wnl.lemmatize(word.decode('utf-8'))
    stemmed_words.append(stemmed_word.encode('utf-8'))

    if stemmed_word not in stop:
        if stemmed_word not in wordcount:
            wordcount[stemmed_word] = 1
        else:
            wordcount[stemmed_word] += 1

counts = wordcount.items()
sorted_counts = sorted(counts, key=operator.itemgetter(1))

open('filter/hottest_singleword.txt', 'w').close()

for k, v in sorted_counts:
    print k.encode('utf-8'), v
    with open('filter/hottest_singleword.txt', 'a') as writing_file:
        writing_file.write(k.encode('utf-8') + ' [' + str(v) + ']' + '\n')

# Find one relative word('BigramAssocMeasures()'') of a word, according to the interval between them (
# 'window_size=7').
bigram_measures = nltk.collocations.BigramAssocMeasures()
# trigram_measures = nltk.collocations.TrigramAssocMeasures()

# (TODO) Still have some encoding error..
finder = BigramCollocationFinder.from_words(stemmed_words, window_size=2)
finder.apply_freq_filter(3)
# Here print Ascii String
print finder.nbest(bigram_measures.pmi, 20)
finder_buffer = finder.nbest(bigram_measures.pmi, 20)
with open('filter/hottest_words.txt', 'w') as writing_file:
    for relative_words in finder_buffer:
        writing_file.write(relative_words[0] + '  ' +relative_words[1] + '\n')
    
