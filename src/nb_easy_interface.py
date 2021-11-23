import nb_nlp
import nb_networkx # Doesn't work with windows due to circular import
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
# Threading_class = nb_threading.nlThreadHandler()
String_class = nl_strings.StringHandler()

# INCLUDE IN DOCS THAT MULTITHREADED FUNCTIONS HAVE 'multithread_' PREFIX
def multithread_search_through_file(
    count : int,
    context_word_single : str,
    # sql_obj_words : nb_sql_parser.Sqlobj_for_words,
    context_words_list : list[str],
    # sql_obj_temp : nb_sql_parser.Sqlobj
    ):

  # Sql_obj_init
  sql_obj_words = nb_sql_parser.Sqlobj_for_words(file_path = f"./.sql_data/{sql_filename_words}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  sql_obj_temp = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename_legal}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  # Deleting already checked words just in case
  if (sql_obj_words.search_if_word_exists([context_word_single])):
    return

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


def multithread_extract_words_files(f : str,
                                    # sql_obj : nb_sql_parser.Sqlobj,
                                    # sql_filename_legal : str,
                                    data_folder : str = "../.data2/"):
  # print(f"File Name : {f}")
  folder = nb_nlp.Folder(data_folder)
  file = folder.File(folder_path=folder.folder_path, file_name = f)
  file.read_file()
  try:
    file.parse_file()
    data = [file.file_name, file.get_nwds_as_str(), file.parties_involved[0],
            file.parties_involved[1],
            file.date_of_judgement.timestamp(),
            file.judge_involved]
    return data
    # sql_obj.commit_to_db() # A commit show not be required for being threadsafe
  except KeyboardInterrupt:
    raise Exception("STOPPED EXECUTION MANUALLY")
  except IndexError:
    return None
  except Exception as e:
    print(e)
    return None
    # fail_count += 1
    # failed_files.append(f)


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


def create_database(files : list[str], sql_filename : str,
                    show_content : bool = False, no_of_threads : int = 1):
  sql_obj = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename}",
                                 conn_type= nb_sql_parser.Conn_type.FILE)

  sql_obj.init_def_file()
  # count = 1
  # fail_count = 0
  # failed_files = []

  print("Creating database from legal words")

  batches_files = [files[no_of_threads * i : no_of_threads * i + no_of_threads]
                  for i in range(int(len(files) / no_of_threads) +
                                 (1 if len(files) % no_of_threads else 0))]
  size_of_batch_files = len(batches_files)

  for i in tqdm.tqdm(range(size_of_batch_files)):
    files = batches_files[i]
    size_of_file_batch = len(batches_files[i])
    # count += 1

    threads = [nb_threading.nlReturnValueThread(target=multithread_extract_words_files, kwargs={
      "f" : files[idx], # "sql_filename_legal" : sql_filename, "sql_obj" : sql_obj
      }) for idx in range(size_of_file_batch)]

    [thread.start()     for thread in threads]
    vals = [thread.join()      for thread in threads]

    vals = [val for val in vals if val != None]

    sql_obj.add_multiple_to_file(data = vals)
    sql_obj.commit_to_db()



  if (show_content):
    sql_obj.read_all_entries()
  del sql_obj

  # print(f"Failed files : {failed_files}")
  # print(f"Failed files count : {fail_count}")

def create_database_words(sql_filename_legal : str, sql_filename_words : str,
                          top_words : int = 20,
                          batch_words : int = 20):
  sql_obj = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename_legal}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  sql_obj_words = nb_sql_parser.Sqlobj_for_words(file_path = f"./.sql_data/{sql_filename_words}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  sql_obj_words.init_def_files()

  sql_obj.cursor.execute("SELECT COUNT(FileName) FROM legaldb")
  total_number = sql_obj.cursor.fetchone()[0]
  sql_obj.cursor.execute("SELECT FileName, ContextWords FROM legaldb")

  wchandl = nb_nlp.Word_Word_Instance()

  for count in tqdm.tqdm(range(total_number)):
    # print(f"\n{count} / {total_number}", end=':')
    data = sql_obj.cursor.fetchone()
    # if (data == No:
    #   break
    # context_words_list = [x for x in data[1].split('|') if len(x) > 0]
    context_words_list = String_class.separate_into_list(data[1], separator='|')

    # delete some top_words here - lets do that later
    combinations_context_words = itertools.combinations_with_replacement(context_words_list, 2)

    for word_instance in combinations_context_words:
      # Type of dict keys chosen is word1-word2
      word = f'{word_instance[0]}-{word_instance[1]}'

      if word in wchandl:
        wchandl[word] += 1
      else :
        wchandl[word] = 1

      del word

    del combinations_context_words

  with open("../notes/count_data.data", 'w') as f:
    f.write(str(wchandl))

  print(wchandl)
  # sql_obj_words.show_all_words()

def get_most_common_words(sql_filename : str):
  sql_obj = nb_sql_parser.Sqlobj(file_path = f"./.sql_data/{sql_filename}",
                                 conn_type = nb_sql_parser.Conn_type.FILE)

  word_count = dict()
  total_number = sql_obj.get_total_number_of_entries()

  sql_obj.cursor.execute("SELECT ContextWords FROM legaldb")


  for i in tqdm.tqdm(range(int(total_number))):
    data = sql_obj.cursor.fetchone()
    separated_list = String_class.separate_into_list(string_data= data[0], separator="|")
    for word in separated_list:
      if word in word_count.keys():
        word_count[word] += 1
      else:
        word_count[word] = 1


  with open("../notes/test_main.data", 'w') as f:
    f.write(str(word_count))


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
