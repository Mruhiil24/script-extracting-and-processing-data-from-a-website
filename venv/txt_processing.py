# importing necessary packages
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
import gensim.corpora as corpora
from pprint import pprint
import os
import gensim
import pickle
import pyLDAvis
from gensim.utils import simple_preprocess


# cleaning the text input file
def txt_clean(word_list, stopwords, min_len):
    clean_words = []
    for line in word_list:
        parts = line.strip().split()
        for word in parts:
            word_l = word.lower()
            if word_l not in stopwords:
                if word_l.isalpha():
                    if len(word_l) > min_len:
                        clean_words.append(word_l)
    return clean_words


txt_file = open('/Users/monekaruhiil/PycharmProjects/project_selenium/article_text.txt', 'r', encoding='utf8')
stopwords_file = open('/Users/monekaruhiil/PycharmProjects/project_selenium/stopwords_en.txt', 'r', encoding='utf8')

# initializing lists
stopwords_list = []
txt_words = []
punctuation_list = [".", ",", ":", ";", "?", "(", ")", "[", "]", "'", "!", "-", "/", "$"]

# populating the list of stopwords
for word in stopwords_file:
    stopwords_list.append(word.strip())

# updating the stopword list
stopwords_list.extend(['people', 'year', 'US', 'U', 'S', 'Will', 'new', 'will'])

for word in txt_file:
    txt_words.append(word.strip())

# setting the minimum word length
min_len = 3

# cleaning the words and getting the list of unique words
clean_words = txt_clean(txt_words, stopwords_list, min_len)

# calculating the sentiment using vader library
analyzer = SentimentIntensityAnalyzer()

# vader needs strings as input. Transforming the list into string
clean_text_str = ' '.join(clean_words)

vad_sentiment = analyzer.polarity_scores(clean_text_str)

pos = vad_sentiment['pos']
neg = vad_sentiment['neg']
neu = vad_sentiment['neu']

# print('\nThe following is the distribution of the sentiment for the file')
# print('\n-- It is positive for', '{:.1%}'.format(pos))
# print('\n-- It is negative for', '{:.1%}'.format(neg))
# print('\n-- It is neutral for', '{:.1%}'.format(neu), '\n')

# calculate bigrams
# bigrammed = list(nltk.bigrams(clean_words))
# print('\n--The following are the bigrams extracted from the text:')
# print(bigrammed)
#
# # print 5 most common bigrams and their frequencies
# freqdist = nltk.FreqDist(bigrammed).most_common(10)
# print('\n--The most frequent bigrams and their frequencies from the text file are as follows: \n', freqdist)

# defining the wordcloud parameters
wc = WordCloud(background_color='white', max_words=4000)

str_word = ''.join(clean_text_str)
# generating word cloud
wc.generate(str_word)

# show the clouds
plt.imshow(wc)
plt.axis('off')
plt.title('word Cloud')
# plt.show()
# plt.savefig('word_Cloud.png')

print("\n--This is end of processing--", )



### LDA processing

# Create Dictionary
id2word = corpora.Dictionary([clean_text_str.split()])

# Create Corpus
texts = [clean_text_str.split()]

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
print(corpus[:1][0][:30])

# number of topics
num_topics = 10

# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)

# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

# Visualize the topics
pyLDAvis.enable_notebook()

LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))

# # this is a bit time consuming - make the if statement True
# # if you want to execute visualization prep yourself
if 1 == 1:
    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)

# load the pre-prepared pyLDAvis data from disk
with open(LDAvis_data_filepath, 'rb') as f:
    LDAvis_prepared = pickle.load(f)

pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')

