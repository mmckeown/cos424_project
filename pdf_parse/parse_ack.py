#!/usr/bin/python

import sys, os
import tempfile
import re
import string

def cleanup_line (line) :
    # Remove page break characters
    clean_line = re.sub("\f", "", line)
    
    # Remove roman numeralsi
    clean_line = re.sub("(\A|\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})(\b|\n)", "", clean_line)
    clean_line = re.sub("(\A|\b)m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})(\b|\n)", "", clean_line)

    return clean_line

def parse_ack (filename) :
    # Convert pdf file to text file
    os.system("pdftotext -f 1 -l 50 " + filename)
    
    # Get output filename
    txt_contents = filename[:-3] + "txt"

    # Process pdf contents
    contents = open(txt_contents, "r")
    in_ack = False
    ack_page_begin = 0
    page_line = 0
    page_count = 1
    acknowledgement_text = ""
    success = True
    for line in contents:
        if not "\f" in line :
            page_line += 1
        else :
            page_line = 1
            page_count += 1

        # Create a stripped line where we remove 
        # page breaks, digits, punctuation, some weird
        # utf-8 or unicode character, roman numerals, 
        # whitespace, and convert all characters to lower 
        # case to compare headings to identify the acknowledgment section
        stripped_line = re.sub("\f", "", line)
        stripped_line = re.sub("[0-9]", "", stripped_line)
        stripped_line = re.sub("[%s]" % re.escape(string.punctuation), "", stripped_line)
        stripped_line = re.sub("\xC2\xA0", "", stripped_line)
        stripped_line = re.sub("\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b", "", stripped_line)
        stripped_line = re.sub("\bm{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\b", "", stripped_line)
        stripped_line = "".join(stripped_line.split())
        stripped_line = stripped_line.lower()
        if not in_ack :
            if stripped_line == "acknowledgment" or \
               stripped_line == "acknowledgement" or \
               stripped_line == "acknowledgments" or \
               stripped_line == "acknowledgements" or \
               stripped_line == "aknowledgment" or \
               stripped_line == "aknowledgement" or \
               stripped_line == "aknowledgments" or \
               stripped_line == "aknowledgements" :
                in_ack = True
                ack_page_begin = page_count
        else :
            if stripped_line == "tableofcontents" or \
               stripped_line == "contents" or \
               stripped_line == "dedication" or \
               stripped_line == "abstract" or \
               stripped_line == "abstractofthedissertation" or \
               stripped_line == "abstractofdissertation" or \
               stripped_line == "abstractofthethesis" or \
               stripped_line == "abstractofthesis" or \
               stripped_line == "chapter" or \
               stripped_line == "chapteri" or \
               stripped_line == "chapterone" or \
               stripped_line == "chapterintroduction" or \
               stripped_line == "chapteroneintroduction" or \
               stripped_line == "introduction" or \
               stripped_line == "curriculumvitae" or \
               stripped_line == "vita" or \
               stripped_line == "publications" or \
               stripped_line == "presentations" or \
               stripped_line == "publicationsandpresentations" :
                # The beginning and end of an acknowledgment
                # should not be on the same page, i.e. no two
                # headings should be on the same page
                if ack_page_begin != page_count :
                    break
                else :
                    # Continue looking if headings are on the same
                    # page, this is likely the table of contents
                    in_ack = False
                    acknowledgement_text = ""
            # Restart if we found another acknowledgement
            # heading, the first was likely in the ToC
            elif stripped_line == "acknowledgment" or \
                 stripped_line == "acknowledgement" or \
                 stripped_line == "acknowledgments" or \
                 stripped_line == "acknowledgements" or \
                 stripped_line == "aknowledgment" or \
                 stripped_line == "aknowledgement" or \
                 stripped_line == "aknowledgments" or \
                 stripped_line == "aknowledgements" :
                ack_page_begin = page_count
            # If we exceed a certain page number, give up
            elif (page_count - ack_page_begin) > 5 :
                success = False
                break;
            else :
                clean_line = cleanup_line(line)
                if not clean_line.isspace():
                    acknowledgement_text += (clean_line)
    contents.close()

    # Remove the converted file
    os.remove(txt_contents)

    return success, acknowledgement_text 


def parse_ack_main() :
    # Parse command line arguments
    if len(sys.argv[1:]) != 1:
        print "Usage: " + sys.argv[0] + " <path to thesis pdf>"
        sys.exit()
    pdf_path = sys.argv[1]
    
    # Parse the acknowledgement section
    print "Parsing acknowledgement section from " + pdf_path + "..."
    success, ack_text = parse_ack(pdf_path)
    if success:
        print ack_text
    else :
        print "ERROR: Acknowledgement exceeded page limit, gave up"

if __name__ == "__main__" :
    parse_ack_main ()
