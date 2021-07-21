import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
from textblob import Word

# BASIC FEATURE EXTRACTION
train = pd.read_csv('tapas_scraped_data_announcements.csv')
print(train.head())

# Number of words
train['word_count'] = train['Leading Post'].apply(lambda x: len(str(x).split(" ")))
print(train[['Leading Post','word_count']].head())

# Number of characters:
train['char_count'] = train['Leading Post'].str.len()
print(train[['Leading Post', 'char_count']].head())

# calculates the average word length in a sentence
def avg_word(sentence):
    words = sentence.split()
    return(sum(len(word) for word in words)/len(words))

# x represents a sentence
train['avg_word_len'] = train['Leading Post'].apply(lambda x: avg_word(x))
print(train[['Leading Post', 'avg_word_len']].head())

stop = stopwords.words('english')
print(stop[:10])

# count the number of stop words in each leading post
train['stopwords'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x in stop]))
print(train[['Leading Post', 'stopwords']].head())

# calculate the number of hashtags in a post
train['hashtags'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
print(train[['Leading Post', 'hashtags']].head())

# calculate the number of mentions in a post
train['mentions'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.startswith('@')]))
print(train[['Leading Post', 'mentions']].head())

# calculate the number of numbers in a post
train['numbers'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
print(train[['Leading Post', 'numbers']].head())

# calculates the number of uppercase letters in a Post
train['num_uppercase'] = train['Leading Post'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
print(train[['Leading Post', 'num_uppercase']])

# BASIC PRE - PROCESSING
# convert all letters to lowercase
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ". join(x.lower() for x in x.split()))
print(train['Leading Post'].head())

# remove all punctuation
train['Leading Post'] = train['Leading Post'].str.replace('[^\w\s]','')
print("remove all punctuation")
print(train['Leading Post'].head())

# remove all stop stopwords
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
print(" remove all stop stopwords")
print(train['Leading Post'].head())

# find the most common words
freq = pd.Series(' '.join(train['Leading Post']).split()).value_counts()[:10]
# and now remove the most common words
train_data = train.copy()
freq = list(freq.index)
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
print("remove the most common words")
print(train['Leading Post'].head())

# find the rarest words

freq = pd.Series(' '.join(train['Leading Post']).split()).value_counts()[-10:]
# remove 'em
freq = list(freq.index)
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
print("remove the rarest words")
print(train['Leading Post'].head())

# spelling corrections

train['Leading Post'][:5].apply(lambda x: str(TextBlob(x).correct()))
print("spelling corrections")
print(train['Leading Post'].head())

# tokenization (word blob)
nltk.download('punkt')
TextBlob(train['Leading Post'][1]).words
print("tokenization - make a word blob")
print(train['Leading Post'].head())

# lemmatizing - converting each word to its root word
nltk.download('wordnet')
train['Leading Post'] = train['Leading Post'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
print("lemmatizing - converting each word to its root word")
print(train['Leading Post'].head())
