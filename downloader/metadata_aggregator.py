import pickle
import sys, os

def aggregate_metadata(dir):
  full_dict = dict()
  for fname in os.listdir(dir):
    if (fname[-6:] == '.pyobj') and (fname.find('all_metadata') < 0) and (fname.find('multipage_metadata') < 0) :
      fp = open(os.path.join(dir,fname))
      partial_dict = pickle.load(fp)
      full_dict[os.path.join(dir,fname[:-15] + ".pdf")] = partial_dict
      fp.close()
      
  return full_dict

