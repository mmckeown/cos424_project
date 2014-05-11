import requests, urllib2
from bs4 import BeautifulSoup as bs
import sys, os
import re
import pickle

def stack_scraper(uni_name, output_dir, page=1, pos=1):
  pdfs = dict()
  for i in range(0,100,5):
    partial_dict = uni_scrape(uni_name, output_dir, page, pos+i)
    pdfs.update(partial_dict)
    
  dir_query_title = re.sub("\"", "", uni_name)
  dir_query_title = re.sub(" ", "_", dir_query_title)
  try:
    dict_file = open(os.path.join(output_dir, dir_query_title, 'all_metadata.pyobj'))
    pickle.dump(pdfs,file_allmeta)
    dict_file.close()
  except:
    print("Tried to write out full metadata dictionary, but failed.")
    
  return pdfs

def uni_scrape(uni_name, output_dir, page=1, pos=1, num=5):
  s = requests.session()
  base_url = 'http://search.proquest.com/'
  results_url = base_url + '/pqdtft/results/CA0B51DFD4B24080PQ/'+str(page)+'/$5bqueryType$3dadvanced:pqdtft$3b+sortType$3dDateDesc$3b+searchTerms$3d$5b$3cschoolName$3dAND$7csch:Exact$28$22' + urllib2.quote(uni_name) +'$22$29$3e$5d$3b+searchParameters$3d$7bNAVIGATORS$3dnavsummarynav,languagenav$28filter$3d200$2f0$2f*$29,decadenav$28filter$3d110$2f0$2f*,sort$3dname$2fascending$29,yearnav$28filter$3d1100$2f0$2f*,sort$3dname$2fascending$29,yearmonthnav$28filter$3d120$2f0$2f*,sort$3dname$2fascending$29,monthnav$28sort$3dname$2fascending$29,daynav$28sort$3dname$2fascending$29,+RS$3dOP,+flags$3dORIGINALEMPTY+FT,+chunkSize$3d100,+instance$3dprod.academic,+ftblock$3d740842+1+660848+670831+194104+194001+670829+194000+660843+660840+104,+removeDuplicates$3dtrue$7d$3b+metaData$3d$7bUsageSearchMode$3dAdvanced,+dbselections$3d10000011,+SEARCH_ID_TIMESTAMP$3d1399784603543,+fdbok$3dN,+siteLimiters$3dManuscriptType,_$25Language$7d$5d?source=fedsrch'# + '&accountID=' + str(accountID)
  print('Loading %s' % results_url)
  results = s.get(results_url)
  print("Response code %d" % results.status_code)
  if page > 1:
    results_url = base_url + '/results.bottompagelinks:gotopage/2?site=pqdtft&t:ac=F14A376B04AC4960PQ/1'
    print('Loading %s' % results_url)
    results = s.get(results_url)
    print("Response code %d" % results.status_code)
    
  results_soup = bs(results.text)
  pdfelems = results_soup.find_all('a',href=re.compile('fulltext'),class_=re.compile('format_pdf'))
  
  pdfs = dict()
  dir_query_title = re.sub("\"", "", uni_name)
  dir_query_title = re.sub(" ", "_", dir_query_title)
  errors = 0
  
  for j, pdfelem in enumerate(pdfelems):
    if errors >=3:
      print('Three consecutive errors. Discontinuing download process.')
      break
    i = j + 100 * (page - 1)
    if j < pos - 1:
      continue
    if j >= pos + num - 1:
      print("Finished set of %d" % num)
      break
    pdfpage_url = base_url + pdfelem['href']
    abspage_url = base_url + pdfelem.parent.parent.select('a.format_abstract')[0]['href']
    
    resp_abs = s.get(abspage_url)
    if resp_abs.status_code != 200:
      print("Error -- abstract page query returned code %d" % (resp_abs.status_code,))
      print("Url was %s" % (abspage_url))
      print("Raising exception if necessary...")
      resp_abs.raise_for_status()
      
    soup_abs = bs(resp_abs.text)
  
    index_dict = dict()   
    info_rows = soup_abs.select('.display_record_indexing_row')
    for row in info_rows:
      index_fieldname = row.select('div')[0].text.encode('ascii','ignore').strip()
      index_dict[index_fieldname] = []
      for index_result in row.select('div')[1].select('span'):
        index_dict[index_fieldname].append(index_result.text.encode('ascii','ignore').strip())
      for index_result in row.select('div')[1].select('a'):
        index_dict[index_fieldname].append(index_result.text.encode('ascii','ignore').strip())
      if len(index_dict[index_fieldname]) == 0:
        index_dict[index_fieldname].append(row.select('div')[1].text.encode('ascii','ignore').strip())
  
    # Load page with embedded PDF
    resp2 = s.get(pdfpage_url)
    if resp2.status_code != 200:
      print("Error -- embedded PDF page query returned code %d" % (resp2.status_code,))
      print("Url was %s" % (pdfpage_url))
      print("Raising exception if necessary...")
      resp2.raise_for_status()
    
    # Analyse page with embedded PDF. Pull PDF url from 'open with your PDF reader' links.
    soup = bs(resp2.text)
    try:
      url = soup.find_all('a',text='open with your PDF reader')[0].attrs['href']
    except IndexError:
      print("Primary link to pdf file failed. Trying backup link.")
      file_page = open(os.path.join(output_dir, dir_query_title, 'errorpage%d.html' %i), 'w')
      file_page.write(resp2.text.encode('ascii','ignore'))
      file_page.close()
      try:
        url = soup.find_all('embed', id='EmbedFile')[0].attrs['src']
      except IndexError:
        print("Tried backup link -- failed")
        errors += 1
        continue
    errors = 0
    
    # Finally! Load the actual file
    resp3 = s.get(url)
    if resp3.status_code != 200:
        print("Error -- embedded PDF page query returned code %d" % (resp2.status_code,))
        print("Search url was %s" % (pdfpage_url))
        print("Raising exception if necessary...")
        resp3.raise_for_status()
    
    # Write file out to disk
    print('Writing PDF from response %d to disk...' % i)
  
    dir_query_title = re.sub("\"", "", uni_name)
    dir_query_title = re.sub(" ", "_", dir_query_title)
    try:
        file = open(os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i), 'w')
    except IOError:
        os.makedirs(os.path.join(output_dir, dir_query_title))
        file = open(os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i), 'w')
    file_meta = open(os.path.join(output_dir, dir_query_title, 'response%d_metadata.pyobj' % i), 'w')
    pickle.dump(index_dict, file_meta)
    file_meta.close()
    pdfs[os.path.join(output_dir, dir_query_title, 'response%d.pdf' % i)] = index_dict
    file.write(resp3.content)
    file.close()
  return pdfs
  
def uni_scrape_main():
    # Parse command line arguments
    if len(sys.argv[1:]) < 2:
        print "Usage: " + sys.argv[0] + " <uni name> <output dir> [results page] [pos]"
        sys.exit()
    pars = sys.argv[1:]
    stack_scraper(*pars)

if __name__ == "__main__":
    uni_scrape_main()