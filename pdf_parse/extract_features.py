#!/usr/bin/python

import sys, os
import re
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

import parse_ack
import parse_words

def extract_features (text, pos_words, neg_words, remove_utf8) :
    # Clean up text (remove punctuation, etc.)

    # Convert everything to lower case
    clean_text = text.lower()
    # Remove page and line breaks
    clean_text = re.sub("[\f]", "", clean_text)
    clean_text = re.sub("[\n]", " ", clean_text)
    # Remove digits
    clean_text = re.sub("[0-9]", "", clean_text)
    # Remove punctuation
    clean_text = re.sub("[%s]" % re.escape(string.punctuation), "", clean_text)
    # Remove utf-8 characters
    if remove_utf8 :
        clean_text = clean_text.decode("utf-8")
        clean_text = clean_text.encode("ascii","ignore")

    # Split words by whitespace
    word_list = clean_text.split()

    # Get word count
    word_count = len(word_list)

    # Remove stop words
    word_list = [w for w in word_list if not w in stopwords.words('english')]

    # Do stemming
    lmtzr = WordNetLemmatizer()
    word_list = [lmtzr.lemmatize(word) for word in word_list]

    # Get bag of words, number of positive words, number
    # of negative words
    bag_of_words = dict()
    pos_words_count = 0
    neg_words_count = 0
    for w in word_list :
        if w in bag_of_words :
            bag_of_words[w] += 1
        else :
            bag_of_words[w] = 1

        if w in pos_words :
            pos_words_count += 1
        if w in neg_words :
            neg_words_count += 1


    return bag_of_words, word_count, pos_words_count, neg_words_count

def extract_features_main () :
    # Parse command line arguments
    if len(sys.argv[1:]) != 1:
        print "Usage: " + sys.argv[0] + " <path to thesis pdf>"
        sys.exit()
    pdf_path = sys.argv[1]

    # Parse the acknowledgement section
    print "Parsing acknowledgement section from " + pdf_path + "..."
    success, ack_text = parse_ack.parse_ack(pdf_path)
    if not success:
        print "Failed to parse acknowledgment section" 
        sys.exit()
    print ack_text

    # Get directory of script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pos_words = parse_words.parse_words (script_dir + "/../opinion-lexicon-English/positive-words.txt")
    neg_words = parse_words.parse_words (script_dir + "/../opinion-lexicon-English/negative-words.txt")

    # Extract the features from the acknowledgement section
    print "Extracting features..."
    bag_of_words, word_count, pos_count, neg_count = extract_features(ack_text, pos_words, neg_words, False)
    print "Acknowledgement section length: " + str(word_count)
    print "     Positive words count: " + str(pos_count)
    print "     Negative words count: " + str(neg_count)
    print bag_of_words

if __name__ == "__main__" :
    extract_features_main ()
