# Importing Interface and Nltk Files
import nltk
from nb_easy_interface import *

def init_nltk() :
  nltk.download('punkt')
  # required for parts of speech tagging
  nltk.download('averaged_perceptron_tagger')

if __name__ == "__main__":

  # init_nltk()

  # files = get_first_n_files(number=20000)

  # create_database(files = files, sql_filename = 'legal_db7.db')

  create_database_words(sql_filename_legal='legal_db7.db', sql_filename_words='words_20000.db', top_words=25)

  # search_interface('words_big.db')
