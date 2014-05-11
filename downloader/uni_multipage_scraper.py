#!/usr/bin/python

import sys, os
import re

import uni_scraper

def uni_multipage_scraper_main () :
    # Parse command line arguments
    if len(sys.argv[1:]) < 3:
        print "Usage: " + sys.argv[0] + " <uni name> <output dir> <number of pages>"
        sys.exit()
    pars = sys.argv[1:]

    dir_query_title = re.sub("\"", "", pars[0])
    dir_query_title = re.sub(" ", "_", dir_query_title)
    if not os.path.isdir(os.path.join(pars[1], dir_query_title)) :
        os.makedirs(os.path.join(pars[1], dir_query_title))
    uni_scraper.multipage_scraper(pars[0], pars[1], int(pars[2])) 

if __name__ == "__main__" :
    uni_multipage_scraper_main ()
