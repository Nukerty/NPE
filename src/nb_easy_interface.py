import nb_nlp
# import nb_networkx # Doesn't work with windows due to circular import
import nl_strings
import nb_sql_parser
import nb_converter
import nb_threading

import os
import time
import shutil
import threading
import itertools
import random
import tqdm

Converter_class = nb_converter.Converter()

# default_folder_name

def debug_file(file_data):
  print(file_data[5])

def show_graph(graph_name : str):
  graph = nb_networkx.Graph("Imported graph")
  graph.load_graph(graph_name)
  graph.show_graph()

def get_first_n_files(data_dir : str = "../.data2", number : int = 20):
  files = os.listdir(data_dir)[:number]
  return files

def get_defaulted_files(single : bool = True) -> list[str]:
  if (single):
    return ["1953_N_6.txt"]
  return ["2005_P_23.txt", "1953_A_6.txt", "1953_L_9.txt"]


# Can add paths 1 and 2 as parameters for file shift
def get_clean_files(files : list[str]):

  correct_files = []
  ## DEBUG :
  for file in files:
    # nb_nlp.load_file_path("../.data/" + file)
    with open ("../.data/"+file) as f:


      # print(f"FILE NAME : {file}")
      if (data[6].find('1') == 0 and data[0].find('v') > 0):
        if (len(data[2]) == 0):
          if (data[5].find("The Judgement") == 0 or
              data[5].find("The Judgment") == 0 ):
              try:
                  if (time.strptime(data[3], "%d %B %Y")):
                      correct_files.append(file)
                      # shutil.copy2(src="../.data/"+file, dst="../.data2/"+file)
              except:
                  continue

  print(f"{correct_files}")
  print(f"Total amount of correct files : {len(correct_files)}\n")
  print(f"Total amount of files : {len(files)}")

  debug_file(temp_data)

  print(temp_data[5].find("The Judgement"))


def create_graph(files : list[str]):
  graph = nb_networkx.Graph("Base graph")
  folder = nb_nlp.Folder("../.data2/")
  count = 1
  size = len(files)
  for f in files:
    print(f"Number {count}/{size} done")
    count += 1
    file = folder.File(folder_path=folder.folder_path, file_name = f)
    file.read_file()
    file.parse_file()
    # file.show_nwds()

    comb = itertools.combinations(file.noun_words, 2)
    comb_list = tuple(comb)

    graph.add_edges_from(comb_list)

  # graph.sh
  # graph.save_graph("Default-data2")
  # print(graph)


def create_database(files : list[str], sql_filename : str, show_content : bool = False):
  sql_obj = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename}",
                                 conn_type= nb_sql_parser.Conn_type.FILE)

  sql_obj.init_def_file()
  folder = nb_nlp.Folder("../.data2/")
  count = 1
  size = len(files)
  fail_count = 0

  failed_files = []
  print("Creating database from legal words")

  size_of_files = len(files)
  for i in tqdm.tqdm(range(size_of_files)):
    f = files[i]
    # print(f"File Name : {f}")
    count += 1
    file = folder.File(folder_path=folder.folder_path, file_name = f)
    file.read_file()
    try:
      file.parse_file()
      data = [file.file_name, file.get_nwds_as_str(), file.parties_involved[0],
              file.parties_involved[1],
              0,                        # file.date_of_judgement.timestamp(),
              file.judge_involved]

      sql_obj.add_single_to_file(data)
      sql_obj.commit_to_db()
    except KeyboardInterrupt:
      raise Exception("STOPPED EXECUTION MANUALLY")
    except:
      fail_count += 1
      failed_files.append(f)
    # file.show_nwds()

  if (show_content):
    sql_obj.read_all_entries()
  del sql_obj

  print(f"Failed files : {failed_files}")
  print(f"Failed files count : {fail_count}")

def create_database_words(sql_filename_legal : str, sql_filename_words : str,
                          top_words : int = 20,
                          batch_words : int = 20):
  sql_obj = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename_legal}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  sql_obj_words = nb_sql_parser.Sqlobj_for_words(file_path = f"./.sql_data/{sql_filename_words}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  sql_obj_temp = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename_legal}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)
  sql_obj_words.init_def_files()

  sql_obj.cursor.execute("SELECT COUNT(FileName) FROM legaldb")
  total_number = sql_obj.cursor.fetchone()[0]
  sql_obj.cursor.execute("SELECT FileName, ContextWords FROM legaldb")

  for count in range(total_number):
    print(f"\n{count} / {total_number}", end=':')
    data = sql_obj.cursor.fetchone()
    if (data == None):
      break
    context_words_list = data[1].split('|')

    context_words_list = set(context_words_list)
    size_context_word_list = len(context_words_list)




    # First self init of elements
    for idx in tqdm.tqdm(range(size_context_word_list)):

      context_word_single = context_words_list[idx]

      # Deleting already checked words just in case
      if (sql_obj_words.search_if_word_exists([context_word_single])):
        continue

      word_dict = dict()

      Converter_class.add_to_word_dict(context_word_single, context_words_list, word_dict)

      # Multiple loop for word instantiation
      sql_obj_temp.cursor.execute("SELECT * FROM legaldb")
      if (count > 0) :
        sql_obj_temp.cursor.fetchmany(count)
      for count2 in range(count, total_number):
        temp_data = sql_obj_temp.cursor.fetchone()
        # Maybe change the below numbers to some struct var outside
        if context_word_single in temp_data[1].split('|'):
          Converter_class.add_to_word_dict(context_word_single, temp_data[1].split('|'), word_dict)

      sorted_word_dict = sorted(word_dict.items(), key = lambda x : x[1], reverse = True)[:top_words] # Should replace to top 5 or smh
      # TOP NUMBER HERE DECIDE

      del word_dict

      word_list = []
      count_list = []
      for (x,y) in sorted_word_dict:
        word_list.append(x)
        count_list.append(y)

      word_cl = nb_nlp.word(name = context_word_single, definition="", connected_words = word_list,
                            contextwordsprob = count_list, related_files="")

      sql_obj_words.add_new_word(word_cl)
      del word_cl
      del context_word_single

  # sql_obj_words.show_all_words()


def search_interface(sql_filename_words:str = 'words_big.db'):
  sql_word_obj = nb_sql_parser.Sqlobj_for_words(file_path = f"./.sql_data/{sql_filename_words}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)
  print("Welcome to the search interface. To exit out of this we present an option at the last")
  while(True):
    print("Enter search query : ")
    val = input()
    flag : bool = sql_word_obj.search_if_word_exists([val])
    if (flag):
      sql_word_obj.show_top_contents_of_a_word(query = val)
    print("\n\nSearch query not found. Try again ? 1=Yes/0=No/~=Yes")

    if(int(input())):
      continue
    else:
      break
