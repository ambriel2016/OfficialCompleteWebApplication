import errno
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.stem.lancaster import LancasterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re
import os
from collections import Counter


class Nlp:

    @staticmethod
    def central(text):
        text = Nlp.remove_symbols(text)
        text = Nlp.remove_stops(text)
        text = Nlp.remove_unneeded_words(text)
        text = Nlp.clean_up(text)
        return text

    @staticmethod
    def remove_symbols(text):
        new_text = text.lower()
        new_text = word_tokenize(new_text)
        characters = r'!\"$%\'()*,”“.-/;:–+<>=@[\]`’~^_{}•&|?'
        for character in characters:
            while character in new_text:
                new_text.remove(character)
        text = ' '.join(new_text)
        while '/' in text:
            text = text.replace('/', ' ')
        while '·' in text:
            text = text.replace('·', '')

        return text

    @staticmethod
    def remove_stops(text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        filtered_sentence = ' '.join(filtered_sentence).lower()
        return filtered_sentence

    @staticmethod
    def remove_unneeded_words(text):
        remove_words = []
        # open the remove words and get them into an trimmed string that will be made into a list
        path = os.getcwd()
        try:
            # Windows
            # with open(path+"\jobscanner\Remove.txt", "r") as f:
            # Mac
            with open(path+"/jobscanner/Remove.txt", "r") as f:
                for line in f:
                    remove_words.append(line)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

        all_remove_words = ' '.join(remove_words)
        while '  ' in all_remove_words:
            all_remove_words = all_remove_words.replace('  ', ' ')

        token_remove_words = word_tokenize(all_remove_words)
        token_remove_words.sort()

        try:
            # Windows
            # with open(path+"\jobscanner\RemoveOutput.txt", "w+") as f:
            # Mac
            with open(path+"/jobscanner/RemoveOutput.txt", "w+") as f:
                for word in token_remove_words:
                    f.write(word + "\n")
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

        word_tokens = word_tokenize(text)
        filtered_sentence = []
        for w in word_tokens:
            if w not in token_remove_words:
                filtered_sentence.append(w)
        filtered_sentence = ' '.join(filtered_sentence).lower()

        return filtered_sentence

    @staticmethod
    def clean_up(text):
        # loop to remove double spaces and trim string
        while True:
            if '  ' in text:
                text = re.sub(r'  ', r' ', text)
            else:
                break
        while ' \'s' in text:
            text = text.replace('\'s', '')
        text = text.strip()
        return text

    @staticmethod
    def return_dictionary(text):
        reg_word_list = word_tokenize(text)
        word_count_dict = Counter(words for words in reg_word_list)
        return word_count_dict

    @staticmethod
    def return_lemma_dictionary(text):
        lm = WordNetLemmatizer()
        ls = LancasterStemmer()
        lemma_list = []
        word_list = word_tokenize(text)
        for word in word_list:
            lemma_word = lm.lemmatize(word)
            stemmed = ls.stem(lemma_word)
            lemma_list.append(stemmed)
        lemma_count_dict = Counter(words for words in lemma_list)

        return lemma_count_dict
