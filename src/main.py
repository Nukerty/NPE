# Importing Custom Files
import nb_nlp
import nl_strings

# Importing Basic Libraries

import os
import threading

if __name__ == "__main__":
    files = os.listdir("../.data/")
    for file in files:
        nb_nlp.load_file_path("../.data/" + file)
