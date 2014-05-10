#!/usr/bin/python

import sys,os
import re

def parse_words (filename) :
    fp = open (filename, "r")
    
    words = []

    for line in fp :
        if not re.match("\A;", line) :
            words.append (re.sub("\n", "", line))

    fp.close()

    return words

def parse_words_main () :
    # Parse command line arguments
    if len(sys.argv[1:]) != 1:
        print "Usage: " + sys.argv[0] + " <path to words list>"
        sys.exit()
    words_path = sys.argv[1]

    # Parse the words
    print "Parsing words from " + words_path + "..."
    print parse_words (words_path)

if __name__ == "__main__" :
    parse_words_main ()
