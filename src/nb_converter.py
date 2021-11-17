import datetime
import nb_sql_parser
import nb_nlp

class Converter:

    def __init__(self):
        pass

    def pytime_to_unixtime(self, x : datetime.datetime = datetime.datetime.fromisoformat('1950-01-01')) -> int:
        # Setting default time to 1950 since data from that time doesn't exist
        return int(x.timestamp())

    def sqlword_to_word(self, sql_query_res : list[str,str,str,str]) -> nb_nlp.word:
        return nb_nlp.word(name = sql_query_res[0], definition="", connected_words=sql_query_res[1].split('|'),
                    contextwordsprob = sql_query_res[2].split('|'), related_files = sql_query_res.split('|'))

    def add_to_word_dict(self, word_name : str, word_list : list[str], word_dict : dict):
        for word in word_list:

        # Deleting cases where the word == the same word in the same file context
            if (word == word_name):
                continue

            if (word in word_dict.keys()):
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    def __del__(self):
        pass
