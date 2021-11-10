# Importing Interface and Nltk Files
import nltk
from nb_easy_interface import *

def init_nltk() :
  nltk.download('punkt')
  # required for parts of speech tagging
  nltk.download('averaged_perceptron_tagger')

if __name__ == "__main__":

  init_nltk()

  files = get_first_n_files()

  create_database(files = files, sql_filename = 'legal_db4.db')
