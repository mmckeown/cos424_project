#!/usr/bin/python

import sys, os
import tempfile
import re

def cleanup_line (line) :
    # Remove page break characters
    clean_line = re.sub("\f", "", line)
    
    # Filter utf-8  characters
    #clean_line = clean_line.decode("utf-8")
    #clean_line = clean_line.encode("ascii","ignore")

    return clean_line

def parse_ack (filename) :
    # Convert pdf file to text file
    os.system("pdftotext -f 1 -l 20 " + filename)
    
    # Get output filename
    txt_contents = filename[:-3] + "txt"

    # Process pdf contents
    contents = open(txt_contents, "r")
    in_ack = False
    page_line = 0
    acknowledgement_text = ""
    for line in contents:
        if not "\f" in line :
            page_line += 1
        else :
            page_line = 1

        # Create a stripped line where we remove 
        # page breaks, colons, whitespace, and convert
        # all characters to lower case to compare
        # headings to identify the acknowledgment section
        stripped_line = re.sub("\f", "", line)
        stripped_line = re.sub(":", "", stripped_line)
        stripped_line = "".join(stripped_line.split())
        stripped_line = stripped_line.lower()
        if not in_ack :
            if stripped_line == "acknowledgment" or \
               stripped_line == "acknowledgement" or \
               stripped_line == "acknowledgments" or \
               stripped_line == "acknowledgements" :
                in_ack = True
                #sys.stdout.write(cleanup_line(line))
                acknowledgement_text += cleanup_line(line)
        else :
            if stripped_line == "tableofcontents" or \
               stripped_line == "dedication" or \
               stripped_line == "abstract" or \
               stripped_line == "abstractofthedissertation" or \
               stripped_line == "abstractofdissertation" or \
               stripped_line == "abstractofthethesis" or \
               stripped_line == "abstractofthesis" or \
               stripped_line == "chapter1" or \
               stripped_line == "chapteri" or \
               stripped_line == "introduction" :
                break
            else :
                #sys.stdout.write(cleanup_line(line))
                acknowledgement_text += (cleanup_line(line))
    contents.close()

    # Remove the converted file
    os.remove(txt_contents)

    return acknowledgement_text


def parse_ack_main() :
    # Parse command line arguments
    if len(sys.argv[1:]) != 1:
        print "Usage: " + sys.argv[0] + " <path to thesis pdf>"
        sys.exit()
    pdf_path = sys.argv[1]
    
    # Parse the acknowledgement section
    print "Parsing acknowledgement section from " + pdf_path + "..."
    print parse_ack(pdf_path)

if __name__ == "__main__" :
    parse_ack_main ()
