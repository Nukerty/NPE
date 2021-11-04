# Importing Custom Files
import nltk
import networkx
import nb_nlp
import nb_networkx
import nl_strings

# Importing Basic Libraries

import os
import time
import shutil
import threading
import itertools

def debug_file(file_data):
  print(file_data[5])

def init_nltk() :
  nltk.download('punkt')
  # required for parts of speech tagging
  nltk.download('averaged_perceptron_tagger')

if __name__ == "__main__":
  init_nltk()

  graph = nb_networkx.Graph("Imported graph")
  graph.load_graph("Default3")
  graph.show_graph()
  



  # # files = os.listdir("../.data2/")[:20]
  # # files = ["2005_P_23.txt", "1953_A_6.txt", "1953_L_9.txt"]
  # files = ["1953_N_6.txt"]
  # correct_files = []

  # folder = nb_nlp.Folder("../.data2/")

  # graph = nb_networkx.Graph("Base graph")
  # count = 1
  # size = len(files)
  # for f in files:
  #   print(f"Number {count}/{size} done")
  #   count += 1
  #   file = folder.File(folder_path=folder.folder_path,
  #       file_name = f)
  #   file.read_file()
  #   file.parse_file()
  #   # file.show_nwds()

  #   comb = itertools.combinations(file.noun_words, 2)
  #   comb_list = tuple(comb)

  #   graph.add_edges_from(comb_list)

  # # graph.show_graph()
  # # graph.save_graph("Default-data2")
  # # print(graph)
  # 

  ## DEBUG :
  # for file in files:
  #   # nb_nlp.load_file_path("../.data/" + file)
  #   with open ("../.data/"+file) as f:

  #     data = f.read().split('\n')

  #     # print(f"FILE NAME : {file}")
  #     if (data[6].find('1') == 0 and data[0].find('v') > 0):
  #       # print(1)
  #       if (len(data[2]) == 0):
  #         # print(2)
  #         if (data[5].find("The Judgement") == 0 or
  #             data[5].find("The Judgment") == 0 ):
  #           # print(3)
  #             try:
  #                 if (time.strptime(data[3], "%d %B %Y")):
  #                     correct_files.append(file)
  #                     # shutil.copy2(src="../.data/"+file, dst="../.data2/"+file)
  #             except:
  #                 continue

  # print(f"{correct_files}")
  # print(f"Total amount of correct files : {len(correct_files)}\n")
  # print(f"Total amount of files : {len(files)}")

  # debug_file(temp_data)

  # print(temp_data[5].find("The Judgement"))


  
        

