"""
Program to process the search_query.
"""

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
#pythofrom spellchecker import SpellChecker
import string
import re

class QueryProcessing():
    def __init__(self, search_string):
        self.search_string = search_string

    def processor(self):
        old_query = self.search_string

        self.search_string = self.search_string.lower()

        translator = str.maketrans('', '', string.punctuation)
        self.search_string = self.search_string.translate(translator)

        self.search_string = " ".join(self.search_string.split())

        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(self.search_string)
        tokens = [word for word in word_tokens if word not in stop_words]

        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]

        #for i in range(len(tokens)):
            #tokens[i] = spell.correction(tokens[i])

        return tokens