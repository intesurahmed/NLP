# -*- coding: utf-8 -*-
"""440Assignment: Text analysis, processing and representation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ydnWfOjolwSGsmOEkO1YAmiugCPDL2jw
"""

pip install nltk

import nltk;
nltk.download('popular')

nltk.download('all')

import nltk
nltk.download('nps_chat')

nltk.download('webtext')

"""##Analyzing word occurrences
####To download Moby Dick, follow these steps:


*   Download books (that we will use to analyze)
*   From nltk.book import *
*   After you do this, variable text1 will contain the entire novella Moby Dick in it.




"""

from nltk.book import *

"""The vocabulary size for Moby Dick. That is, how many unique words are in Moby Dick




"""

vocabulary=set(text1)

vocabulary_size=len(vocabulary)

vocabulary_size

unique_words=set(text1)

len(unique_words)

"""Total words are there in Moby Dick"""

total_words=len(text1)

total_words

"""The number of times a word is present in the novella. Create a python dictionary where the key will be a word and the value will be the number of times that word appeared in Moby Dick. We will consider punctuation marks as words here.

"""

text1

type(text1)

text1.generate()

word_list=sorted(text1)

len(word_list)

from collections import defaultdict

dictionary = defaultdict(int)

for count in word_list:
    dictionary[count] += 1
word_count=dict(dictionary)
print(word_count)

"""List of top 10 most frequent words"""

# top 10 most frequent words
top_10_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]

print(top_10_words)

"""List of top 10 most frequent words that are not punctuation marks"""

# top 10 most frequent words without punctuation
import string

filtered_counts = {word: count for word, count in word_count.items() if word not in string.punctuation}

top_10_words_woutP = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)[:10]
print(top_10_words_woutP)

"""##Loading, cleaning and processing text files
Install Pandas: pip install pandas in terminal
Download this file: https://drive.google.com/file/d/1dbwZBzlFQnuc1tqv0lXvBj9BqTJ_aZMe/view?usp=drive_link
Unzip the file imdb_440.zip. It will contain the actual data file in .csv format. This is a set of reviews from IMDB.

"""

pip install pandas

import pandas as pd
imdb_reviews=pd.read_csv("/content/IMDB Dataset.csv")

total_reviews=len(imdb_reviews)
print(total_reviews)

imdb_reviews

"""Load the csv file using pandas. How many reviews do we have here? Which row has the longest review in terms of words? How about in terms of sentences?

"""

from nltk.tokenize import word_tokenize

previouslen=0
prev_row=0
for row in range(total_reviews):
  words=word_tokenize(imdb_reviews["review"][row])
  wordslength=len(words)
  if wordslength>previouslen:
    previouslen=wordslength
    prev_row=row
print(prev_row)

print(imdb_reviews["review"][prev_row])

from nltk.tokenize import sent_tokenize

previouslen=0
prev_row=0
for row in range(total_reviews):
  sentences=sent_tokenize(imdb_reviews["review"][row])
  sentencelength=len(sentences)
  if sentencelength>previouslen:
    previouslen=sentencelength
    prev_row=row
print(prev_row)

nltk.download('punkt')

"""Cleaning step 1: Now, from each review, remove stopwords and punctuations

"""

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
sentences = []
stop_words = set(stopwords.words('english'))
for row in range(total_reviews):
  cleaned_text = re.sub(r"(?:<br\s*/?>)+", " ", imdb_reviews["review"][row])
  word_tokens = word_tokenize(cleaned_text)
  cleaned_tokens = [re.sub(r'[^\w\s]', '', token) for token in word_tokens if re.sub(r'[^\w\s]', '', token)]
  filtered_sentence = []
  for w in cleaned_tokens:
    if w not in stop_words:
      filtered_sentence.append(w)
  sentences.append(filtered_sentence)

print(sentences[0])

"""Cleaning step 2: Convert the reviews to lowercase and save these clean reviews (only the reviews, not their classes from the csv file) in a text file where each line will be a single review (that is, line 1 will contain the entire first review, line 2 will contain the entire second review and so on. Check whether you have saved all the reviews, or did you miss out on anything."""

lower_sentences=[]
for row in range(len(sentences)):
  lower_sent=[]
  for word in range(len(sentences[row])):
    lower_text = sentences[row][word].lower()
    lower_sent.append(lower_text)
  lower_sentences.append(lower_sent)
print((lower_sentences[0]))

with open('reviews.txt', 'w') as filehandle:
    for listitem in lower_sentences:
        filehandle.write('%s\n' % listitem)

"""## Representation

using scikit-learn’s TF-IDF vectorizer
"""

from sklearn.feature_extraction.text import TfidfVectorizer
corpus=imdb_reviews["review"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
vectorizer.get_feature_names_out()
print(X.shape)

!gdown 14DWN7qZTfTttV1rkeUMJhQ2rLjx7AdD9

"""####word embeddings
Download this file: https://drive.google.com/file/d/14DWN7qZTfTttV1rkeUMJhQ2rLjx7AdD9/view?usp=drive_link
This will have almost all the words in the English language and their GLoVe word embedding in 100-space (that is, each word is represented by 100-dimensional vectors). Load this file and extract the vectors for all the words. Then, find cosine similarities between these vectors:
Man and Woman
Cat and Dog
King and Queen

	 Show that (in your code, using cosine similarity), that the vector you get from King - Man + Woman is close to the vector of Queen, that is, prove this equation: King - Man + Woman = Queen.

"""

import numpy as np


def load_glove_embeddings(file_path):
    embeddings = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            word = parts[0]
            vector = np.array(parts[1:], dtype=np.float32)
            embeddings[word] = vector
    return embeddings
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


glove_file_path = '/content/glove.6B.100d.txt'
glove_embeddings = load_glove_embeddings(glove_file_path)


word_pairs = [("man", "woman"), ("cat", "dog"), ("king", "queen")]


for word1, word2 in word_pairs:
    vec1 = glove_embeddings[word1]
    vec2 = glove_embeddings[word2]
    similarity = cosine_similarity(vec1, vec2)
    print(f"Cosine similarity between '{word1}' and '{word2}': {similarity:.4f}")

king = glove_embeddings["king"]
man = glove_embeddings["man"]
woman = glove_embeddings["woman"]
queen = glove_embeddings["queen"]

king_man_woman = king - man + woman
print(king_man_woman )
print(queen )
similarity = cosine_similarity(king_man_woman, queen)
print(f"Cosine similarity between 'King - Man + Woman' and 'Queen': {similarity:.4f}")

