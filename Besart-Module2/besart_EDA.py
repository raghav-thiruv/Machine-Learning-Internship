import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from collections import defaultdict
from textblob import Word
import nltk
import seaborn as sns


def get_top_ngram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:10]

def show_wordcloud(data):
    wordcloud = WordCloud(
        background_color="white",
        stopwords=stopwords.words("english"),
        max_words=100,
        max_font_size=30,
        scale=3,
        random_state=1)
    wordcloud = wordcloud.generate(str(data))
    fig = plt.figure(1, figsize=(12, 12))
    plt.axis("off")
    plt.imshow(wordcloud)
    plt.show()

if __name__ == '__main__':
    cols_to_use = ["Category", "Title", "Date", "Original Post"]
    stop = stopwords.words("english")

    """ Display options """
    pd.set_option('display.max_columns', None)
    train = pd.read_csv("TapasData - Copy.csv", usecols=cols_to_use)[
        cols_to_use]
    # print(len(train))

    """ Determine # of stop words """
    train["stopwords"] = train["Original Post"].apply(
        lambda x: len([x for x in str(x).split() if x in stop]))
    # print(train[["Original Post", "stopwords"]].head())
    """ Pre-processing """

    train = train.drop(train[train["Original Post"] == "Aberrant HTML"].index)
    # print(len(train))

    train["Original Post"] = train["Original Post"].apply(
        lambda x: " ".join(x.lower() for x in str(x).split()))
    # print(train["Original Post"].head())

    train["Original Post"] = train["Original Post"].str.replace("[^\\w\\s]",
                                                                "", regex=True)
    # print(train["Original Post"].head())

    train["Original Post"] = train["Original Post"].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop))
    # print(train["Original Post"].head())

    most_freq = pd.Series(
        " ".join(train["Original Post"]).split()).value_counts()[
           :20]
    train_data = train.copy()
    most_freq = list(most_freq.index)
    train["Original Post"] = train["Original Post"].apply(
        lambda x: " ".join(x for x in x.split() if x not in most_freq))

    least_freq = pd.Series(
        " ".join(train["Original Post"]).split()).value_counts()[
           -20:]
    least_freq = list(least_freq.index)
    train["Original Post"] = train["Original Post"].apply(
        lambda x: " ".join(x for x in x.split() if x not in least_freq))

    # train["Original Post"].apply(lambda x: str(TextBlob(x).correct()))
    #
    # train["Original Post"] = train["Original Post"].apply(lambda x: " ".join(
    #     [Word(word).lemmatize() for word in x.split()]))

    """ END OF PRE-PROCESSING """

    """ Number of topics per category """
    # print(train.groupby("Category").size())

    """ Word count of each original post, added to dataframe """
    train["word_count_OG"] = train["Original Post"].apply(
        lambda x: len(str(x).split()))
    # print(train[["Original Post", "Category", "word_count_OG"]].head())

    """ Average number of words in the original post per category """
    grouping = train.groupby("Category")
    word_avg_by_category = round(
        grouping["word_count_OG"].sum() / grouping.size())
    # print(word_avg_by_category)

    """ Term frequency """
    tf = (train["Original Post"][1:2]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0).reset_index()
    tf.columns = ["words", "tf"]

    """ Inverse document frequency """
    for i, word in enumerate(tf["words"]):
        tf.loc[i, "idf"] = np.log(train.shape[0]/(len(train[train["Original Post"].str.contains(word)])))
    # print(tf)

    """ Bag of words """
    bow = CountVectorizer(max_features=1000, lowercase=True, ngram_range=(1,1), analyzer="word")
    train_bow = bow.fit_transform(train["Original Post"])
    # print(train_bow)

    """ Sentiment analysis """
    train["Sentiment"] = train["Original Post"].apply(lambda x: TextBlob(x).sentiment[0])
    # print(train[["Original Post", "Sentiment"]].head())

    new = train["Original Post"].str.split()
    new = new.values.tolist()
    corpus = [word for i in new for word in i]

    dic = defaultdict(int)
    for word in corpus:
        if word in stop:
            dic[word] += 1

    top_n_bigrams = get_top_ngram((train["Original Post"]), 2)[:10]
    x,y = map(list, zip(*top_n_bigrams))
    sns.barplot(x=y, y=x)
    plt.show()

    top_tri_grams = get_top_ngram((train["Original Post"]), 3)[:10]
    x, y = map(list, zip(*top_tri_grams))
    sns.barplot(x=y, y=x)
    plt.show()

    """ Word Cloud """
    show_wordcloud(corpus)

    # train.to_csv("TapasData - Copy.csv")


