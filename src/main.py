# Importing Interface and Nltk Files
import nltk
from nb_easy_interface import *

def init_nltk() :
  nltk.download('punkt')
  # required for parts of speech tagging
  nltk.download('averaged_perceptron_tagger')

if __name__ == "__main__":

  # init_nltk()

  # files = get_first_n_files(number=10000)

  # create_database(files = files, sql_filename = 'legal_db_10000_thread_1.db', no_of_threads = 100)

  create_database_words(sql_filename_legal='legal_db4.db', sql_filename_words='words_imp_4.db', top_words=25)

  # get_most_common_words(sql_filename='legal_db7.db')

  # search_interface('words_big.db')
