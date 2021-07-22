# -*- coding: utf-8 -*-
"""
Step one: Read the csv file, which pandas stores as
a two dimensional array with labeled axes.
"""

import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
from textblob import Word
train = pd.read_csv('tapas_scraped_data_announcements.csv')
print(train.head())

"""
The next step is to do some basic feature extraction,
starting with finding the number of words each of the Leading Posts.
Create a new list, corresponding to the word counts, and apply a
function to the the Leading Post column which takes a given string x,
splits into a list of words, and then returns the length of that list.

"""

train['word_count'] = train['Leading Post'].apply(lambda x: len(str(x).split(" ")))

"""
Similarly, let's find the number of characters in each Leading Post

"""

train['char_count'] = train['Leading Post'].str.len()

"""
Now, let's find the average word length in a sentence.
For this, it is simpler to create an outside function.

"""

def avg_word_len(sentence):
  words = sentence.split()
  return(sum(len(word) for word in words)/len(words))

train['avg_word_len'] = train['Leading Post'].apply(lambda x: avg_word_len(x))

"""Stop words are common words that are nothing but a burden to NLP.
 It is best to remove them. """

stop = stopwords.words('english')

train['stopwords'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x in stop]))

"""And now, to calculate the following:


1. the # of numbers per post
2. the # of hashtags per post
3. the # of mentions (@) per post
4. the number of uppercase letters per post


"""

train['num_numbers'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))

train['num_hashtags'] = train['Leading Post'].apply(lambda x: len([ x for x in x.split() if x.startswith('#')]))

train['num_mentions'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.startswith('@')]))

train['num_upper_case'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.isupper()]))

"""## Part Two: Basic Text Preprocessing

Convert all letters to lowercase
"""

train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x.lower() for x in x.split()))

"""remove the stop words

"""

# and now to remove them
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

"""remove all the punctuation

"""
train['Leading Post'] = train['Leading Post'].str.replace('[^\w\s]','')

"""Find the most common words, and then remove them. """

freq = pd.Series(' '.join(train['Leading Post']).split()).value_counts()[:10]

train_data = train.copy()
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))

"""Do the same thing for the rarest words."""

freq = pd.Series(' '.join(train['Leading Post']).split()).value_counts()[-10:]


train['Leading Post'] = train['Leading Post'].apply(lambda x: " ". join(x for x in x.split() if x not in freq))

"""Time for spelling corrections.
For this, we have to use the Textblob library.
(Correcting the spelling for the entire category is very timeconsuming,
so I will only do it for the first 4 for now.)"""

train['Leading Post'][:3].apply(lambda x: str(TextBlob(x).correct()))
train['Leading Post'].head()

"""Tokenization - the process of dividing text into a
sequence of words or sentences. """

nltk.download('punkt')
TextBlob(train['Leading Post'][1]).words

"""Lemmatizing - this converts all words to their root

"""

nltk.download('wordnet')
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
print(train['Leading Post'].head())

"""## Advanced Text Processing :)

An **N - gram** is a combination of multiple words often found together,
and a N-gram model can be used to predict the probability that a word
will occur after a text sequence. For example; an N - gram
( specifically, a bigram) would be something like "Covid-19 pandmenic"
and the probability that "pandemic" will follow "Covid-19" is higher
than "joy" following "Covid-19"
"""

# bigrams
TextBlob(train['Leading Post'][1]).ngrams(2)

# trigrams
TextBlob(train['Leading Post'][1]).ngrams(3)

"""**TF (Text Frequency)** is simply the ratio that a word appears to
the length of the sentence it is present in

> TF = (Number of times term T appears in the particular row) / (number of terms in that row)

Obviously, the higher the TF - the more relevant the word in the given context


"""

tf1 = (train['Leading Post'][1:2]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf1.columns = ['words','tf']
tf1

"""**IDF - inverse document frequency**

> IDF = log(N/n)

where N = # of documents, and n = # of documents a term appears in

*a short guide to numpy (what on earth does .shape[] do?)*


> given an input array, .shape returns the dimensions of that array.
In this example, train.shape[0] returns the number of posts
in the Announcments category (119)

*step by step guide, from in to out*

this line of code returns a boolean, True if the target word is contained
in a a leading post, False otherwise.
```
train['Leading Post'].str.contains(word)]
```
and this returns every row in train where the word is present
```
(train[train['Leading Post'].str.contains(word)])
```
take the length of all the rows where the word is present ... and tah
dah you found n - the number of documents a word appears in
```
len((train[train['Leading Post'].str.contains(word)]))
```
"""

import numpy as np
for i,word in enumerate(tf1['words']):
      tf1.loc[i, 'idf'] = np.log(train.shape[0]/(len(train[train['Leading Post'].str.contains(word)])))
print(tf1)

"""Putting it all together with **TF-IDF: Term Frequency - Inverse Document Frequency**

```
TF-IDF (word, Document#) = TF * IDF
```

The higher the tf - idf score, the more important a word is!
"""

tf1['tf-idf'] = tf1['tf']*tf1['idf']
print(tf1)
