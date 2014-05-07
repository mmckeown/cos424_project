#!/usr/bin/python

import sys, os
import tempfile

def parse_ack (filename) :
    # Convert pdf file to text file
    os.system("pdftotext -f 1 -l 20 " + filename)
    
    # Get output filename
    txt_contents = filename[:-3] + "txt"

    # Process pdf contents
    contents = open(txt_contents, "r")
    for line in contents:
        if "acknowledgment" in line.lower() or \
           "acknowledgement" in line.lower() :
            print line
    contents.close()

    # Remove the converted file
    os.remove(txt_contents)


def parse_ack_main() :
    # Parse command line arguments
    if len(sys.argv[1:]) != 1:
        print "Usage: " + sys.argv[0] + " <path to thesis pdf>"
        sys.exit()
    pdf_path = sys.argv[1]
    
    # Parse the acknowledgement section
    print "Parsing acknowledgement section from " + pdf_path + "..."
    parse_ack(pdf_path)

if __name__ == "__main__" :
    parse_ack_main ()
