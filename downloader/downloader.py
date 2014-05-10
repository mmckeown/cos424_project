## Byron Vickers, 2014

from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import requests
import urllib
import sys, os
import re

## Example arguments:
# title = "Princeton University"
# max_records = "30"
# output_dir = '/Users/Byron/Desktop/delete' # root directory in which PDFs will be saved


def scrape(title, max_records, output_dir):
    # Define search parameters
    search_params = {
        'author' : '',
        'title' : '"%s"' % title # multi-word titles should always be quoted (it seems?)
    }
    
    # Build search query string
    search_str = []
    for (k,v) in search_params.iteritems():
        if v:
            search_str.append(k+'='+v)
    
    search_str = " AND ".join(search_str)
    
    # Full HTTP GET request parameters
    # Most of these are taken copied from http://bibwild.wordpress.com/2014/02/17/a-proquest-platform-api/
    http_params = {
        'operation' : 'searchRetrieve',
        'version' : '1.2',
        'maximumRecords' : max_records,
        'startRecord' : '1',
        'query' : search_str,
    }
    
    # Build URL for query. Currently only for PhD and dissertation database, but easy to tweak
    base_search_url = 'http://fedsearch.proquest.com/search/sru/'
    db = 'pqdtft' # Code for 'ProQuest Dissertations and Theses Full Text' database
    search_url = base_search_url + db + '?' + urllib.urlencode(http_params)
    print("Querying %s" % search_url)
    
    # Set up session. Spoof agent -- not sure if necessary
    s = requests.Session()
    user_agent = {'User-Agent': 'Mozilla/5.0'}
    s.headers.update(user_agent)
    
    # Perform the database query
    resp1 = s.get(search_url)
    if resp1.status_code != 200:
        print("Error -- database query returned code %d" % resp1.status_code)
        print("Search url was %s" % search_url)
        print("Raising exception if necessary...")
        resp1.raise_for_status()
    
    # Analyse xml response. Pull out author name and url for the page with embedded PDF.
    # Currently pulls all authors and urls which have 'fulltext'-indicated links
    root = ET.fromstring(resp1.text.encode('utf8'))
    
    numresponse = int(root[1].text)
    print("%d responses" % numresponse)

    filenames = []
    for i,elem in enumerate(root[2]): # iterate over individual query responses (documents)  
        
        pdfpage_elems = elem.findall(".//*[@tag='856'][@ind2='0']/*[@code='u']")
        
        if(pdfpage_elems):
            pdfpage_url = pdfpage_elems[0].text
            
            # example metadata extraction:
            author = elem.findall(".//*[@tag='100']/*")[0].text
            
            ## Put further XML extractions here.
            
            ## Add export of desired metadata to CSV.
            
            # Load page with embedded PDF
            resp2 = s.get(pdfpage_url)
            if resp2.status_code != 200:
                print("Error -- embedded PDF page query returned code %d" % (resp2.status_code,))
                print("Search url was %s" % (pdfpage_url))
                print("Raising exception if necessary...")
                resp2.raise_for_status()
            
            # Analyse page with embedded PDF. Pull PDF url from 'open with your PDF reader' links.
            soup = bs(resp2.text)
            url = soup.find_all('a',text='open with your PDF reader')[0].attrs['href']
            
            # Finally! Load the actual file
            resp3 = s.get(url)
            if resp3.status_code != 200:
                print("Error -- embedded PDF page query returned code %d" % (resp2.status_code,))
                print("Search url was %s" % (pdfpage_url))
                print("Raising exception if necessary...")
                resp3.raise_for_status()
            
            # Write file out to disk
            print('Writing PDF from response %d to disk...' % i)

            dir_query_title = re.sub("\"", "", search_params['title'])
            dir_query_title = re.sub(" ", "_", dir_query_title)
            try:
                file = open(os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i), 'w')
            except IOError:
                os.makedirs(os.path.join(output_dir, dir_query_title))
                file = open(os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i), 'w')
            filenames.append (os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i))
            file.write(resp3.content)
            file.close()

    return filenames

def scrape_main():
    # Parse command line arguments
    if len(sys.argv[1:]) != 3:
        print "Usage: " + sys.argv[0] + " <title query> <max results> <output dir>"
        sys.exit()
    pars = sys.argv[1:4]
    scrape(*pars)

if __name__ == "__main__":
    scrape_main()
