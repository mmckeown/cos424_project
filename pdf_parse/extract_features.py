#!/usr/bin/python

import sys, os
import re
import string
import parse_ack

def extract_features (text, remove_utf8) :
    # Clean up text (remove punctuation, etc.)

    # Convert everything to lower case
    clean_text = text.lower()
    # Remove page and line breaks
    clean_text = re.sub("[\n\f]", "", clean_text)
    # Remove digits
    clean_text = re.sub("[0-9]", "", clean_text)
    # Remove punctuation
    clean_text = re.sub("[%s]" % re.escape(string.punctuation), "", clean_text)
    # Remove utf-8 characters
    if remove_utf8 :
        clean_text = clean_text.decode("utf-8")
        clean_text = clean_text.encode("ascii","ignore")

    return clean_text

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

    # Extract the features from the acknowledgement section
    print "Extracting features..."
    print extract_features(ack_text, False)

if __name__ == "__main__" :
    extract_features_main ()
