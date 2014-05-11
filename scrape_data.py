#!/usr/bin/python

import sys, os
import re

scrape_data_script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(scrape_data_script_dir + "/downloader")
sys.path.append(scrape_data_script_dir + "/pdf_parse")

import downloader
import parse_ack
import parse_words
import extract_features

def scrape_data (title, max_records, output_dir) :
    # Scrape PDFs
    pdfs = downloader.scrape(title, max_records, output_dir)   
    print str(pdfs)
    
    # Parse the positive and negative words lists
    pos_words = parse_words.parse_words (scrape_data_script_dir + "/opinion-lexicon-English/positive-words.txt")
    neg_words = parse_words.parse_words (scrape_data_script_dir + "/opinion-lexicon-English/negative-words.txt")

    # Iterate over PDFs and process them into features
    pdf_data = dict()
    for pdf in pdfs :
        # Parse acknowledgement section
        print "Parsing acknowledgement section from " + pdf + "..."
        success, ack_text = parse_ack.parse_ack(pdf)
        if success :
            pdf_data[pdf] = dict()
            pdf_data[pdf]["ack_text"] = ack_text
            
            # Extract the features
            print "Extracting features..."
            bag_of_words, word_count, pos_count, neg_count = \
                extract_features.extract_features(ack_text, pos_words, neg_words, True)

            pdf_data[pdf]["bag_of_words"] = bag_of_words
            pdf_data[pdf]["word_count"] = word_count
            pdf_data[pdf]["pos_count"] = pos_count
            pdf_data[pdf]["neg_count"] = neg_count
        else :
            print "Error parsing acknowledgement section...dropping PDF"

    # Create a bag of words CSV
    all_words = set()
    for pdf in pdfs :
        pdf_word_set = set(pdf_data[pdf]["bag_of_words"].keys())
        all_words = all_words.union(pdf_word_set)
    fp = open(output_dir + "/" + re.sub(" ", "_", title) + "/" + "bag_of_words.csv", "w")
    fp.write("docid")
    all_words_list = list(all_words)
    for w in all_words_list :
        fp.write("," + w)
    fp.write("\n")
    for pdf in pdfs :
        fp.write(pdfs[pdf]["ProQuest document ID"][0])
        for w in all_words_list :
            if w in pdf_data[pdf]["bag_of_words"] :
                fp.write("," + str(pdf_data[pdf]["bag_of_words"][w]))
            else :
                fp.write(",0")
        fp.write("\n")
    fp.close() 
     
    # Create a attributes CSV
    fp = open(output_dir + "/" + re.sub(" ", "_", title) + "/" + "attributes.csv", "w")
    fp.write("docid,word_count,pos_count,neg_count")
    attrs = pdfs[pdfs.keys()[0]]
    for attr in attrs :
        if attr != "ProQuest document ID" :
            fp.write("," + attr)
    fp.write("\n")
    for pdf in pdfs :
        fp.write(pdfs[pdf]["ProQuest document ID"][0] + "," + str(pdf_data[pdf]["word_count"]) + "," + \
                 str(pdf_data[pdf]["pos_count"]) + "," + str(pdf_data[pdf]["neg_count"]))
        for attr in attrs :
            if attr != "ProQuest document ID" :
                fp.write(",")
                try:
                    if len(pdfs[pdf][attr]) > 1 :
                        fp.write(re.sub("[,;]", "", pdfs[pdf][attr][0]))
                        for val in pdfs[pdf][attr][1:] :
                            fp.write(";" + re.sub("[,;]", "", val))
                    else :
                        fp.write (re.sub("[,;]", "", pdfs[pdf][attr][0]))
                except:
                    pass
        fp.write("\n")
    fp.close()

def scrape_data_main () :
    # Parse command line arguments
    if len (sys.argv[1:]) != 3 :
        print "Usage: " + sys.argv[0] + " <title query> <max results> <output dir>"
        sys.exit ()
    pars = sys.argv[1:4]
    
    # Scrape the data
    scrape_data(*pars)

if __name__ == "__main__" :
    scrape_data_main()
