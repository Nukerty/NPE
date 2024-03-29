import sqlite3
import os
import enum
import nb_nlp
# import typing

Case_file_details     = list[str, str, str, str, int, str]
word_data             = list[str, str, str, str]
word_count_data       = list[str, str, int, str]

class Conn_type(enum.Enum):
  FILE    = 0
  MEMORY  = 1


class Sqlobj:

  def __init__(self, file_path: str, conn_type: Conn_type):
    self.file_path = file_path
    self.conn_type = conn_type
    # if (os.path.exists(self.file_path)):
    #     print(f"File : {self.file_path} already exists")
    self.conn = sqlite3.connect(file_path if conn_type == Conn_type.FILE else ':memory:',
                                check_same_thread = False)
    self.cursor = self.conn.cursor()

  def ret_cursor(self) -> sqlite3.Cursor :
    # Does this imply multiple instantiation?
    return self.conn.cursor

  def init_def_file(self) -> None:
    try :
      self.cursor.execute(""" CREATE TABLE legaldb (
      FileName        text,
      ContextWords    text,
      PartyOne        text,
      PartyTwo        text,
      DateOfJudgement integer,
      JudgeInvolved   text
      )""")

    except:
      raise Exception("""TABLE ALREADY INTIALIZED. Delete the
      Sqlobj.init_def_file method or check db file for missing params""")


  def add_single_to_file(self, data : Case_file_details) -> None:
    """ADDS SINGLE ELEMENT TO FILE"""
    self.cursor.execute("INSERT INTO legaldb VALUES (?, ?, ?, ?, ?, ?)", data)
  def add_multiple_to_file(self, data : list[Case_file_details]) -> None:
    """ADDS MULTIPLE ELEMENT TO FILE"""
    self.cursor.executemany("INSERT INTO legaldb VALUES (?, ?, ?, ?, ?, ?)", data)


  def commit_to_db(self):
    if (self.conn.in_transaction):
      self.conn.commit()

  def read_all_entries(self):
    self.cursor.execute("SELECT * FROM legaldb")
    rows = self.cursor.fetchall()
    for row in rows:
      print(row)

  def get_all_entries(self) -> list:
    self.cursor.execute("SELECT * FROM legaldb")
    return self.cursor.fetchall()

  def get_all_context_words(self):
    self.cursor.execute("SELECT ContextWords FROM legaldb")
    return self.cursor.fetchall()

  def get_total_number_of_entries(self) -> int:
    self.cursor.execute("SELECT COUNT(*) FROM legaldb")
    return self.cursor.fetchone()[0]


  def __del__(self):
    del self.cursor
    self.conn.close()



class Sqlobj_for_words:

  def __init__(self, file_path: str, conn_type: Conn_type):
    self.file_path = file_path
    self.conn_type = conn_type
    if (os.path.exists(self.file_path)):
      print(f"File : {self.file_path} already exists")
    self.conn = sqlite3.connect(file_path if conn_type == Conn_type.FILE else ':memory:', check_same_thread = False)
    self.cursor = self.conn.cursor()

  def init_def_files(self) -> None:
    # Can add k-words here itself for optimizations but lets keep it that way for now
    try :
      # Metadata to each word
      self.cursor.execute(""" CREATE TABLE words (
      Word                text        UNIQUE,
      ContextWords        text,
      ContextWordsProb    text,
      RelatedFiles        text
      )""")

    except:
      raise Exception("""TABLE ALREADY INTIALIZED. Delete the
      Sqlobj.init_def_file method or check db file for missing params""")

  def add_single_to_file(self, data : word_data) -> None:
    """ADDS SINGLE ELEMENT TO FILE"""
    self.cursor.execute("INSERT INTO words VALUES (?, ?, ?, ?)", data)
  def add_multiple_to_file(self, data : list[word_data]) -> None:
    """ADDS MULTIPLE ELEMENT TO FILE"""
    self.cursor.executemany("INSERT INTO words VALUES (?, ?, ?, ?)", data)

  def search_if_word_exists(self, query : list[str]) -> bool:
    self.cursor.execute("SELECT COUNT(Word) FROM words WHERE Word=(?)", query)
    k = self.cursor.fetchone()
    if (k[0] == 0):
      return False
    return True

  def add_new_word(self, Word : nb_nlp.word):
    if (self.conn.in_transaction):
      self.conn.commit()
    pack = [Word.name, '|'.join(Word.contextwords),
            '|'.join([str(x) for x in Word.contextwordsprob]),""]
    self.cursor.execute("INSERT INTO words VALUES ((?),(?),(?),(?))", pack)
    self.conn.commit()

  def show_top_contents_of_a_word(self, query : str, check_if_exists : bool = False, top_words :int = 20):
    if (check_if_exists):
      search_if_word_exists(query)
    self.cursor.execute("SELECT * FROM words WHERE Word=(?)", query)
    data = self.cursor.fetchone()
    print("Top 5 words are : ")
    words = data[1].split('|')
    words_prob = data[2].split('|')
    # Print comprehension
    _ = [print(f"{word[i]} : {words_prob[i]}") for i in range(top_words)]
    print()


  def show_all_words(self):
    self.cursor.execute("SELECT * FROM words")
    data_all = self.cursor.fetchall()
    for data in data_all:
      print(data)


  # def append_into_exisiting_word(self, word : str, list_of_context_words : list[str],
  #                                count_list_of_words : list[float]) -> None:

  #   # Error check before hand
  #   if len(list_of_context_words) == 0:
  #     raise Exception("Empty list of context words")
  #   if len(count_list_of_words) == 0:
  #     raise Exception("Empty list of context words probabilities")
  #   if len(list_of_context_words) != len(count_list_of_words):
  #     raise Exception("Unequal sizes of word and word prob in consideration")


  #   self.cursor.execute("SELECT ContextWords,ContextWordsProb FROM words WHERE Word=(?)", word)
  #   context_words, context_words_prob = self.cursor.fetchone()
  #
  #   self.cursor.execute("UPDATE words SET ContextWords=(?) WHERE Word=(?)",
  #                       context_words+'|'+'|'.join(list_of_context_words),word)
  #   self.cursor.execute("UPDATE words SET ContextWordsProb=(?) WHERE Word=(?)",
  #                       context_words_prob+'|'+'|'.join(count_list_of_words),word)

  def delete_word(self, word : str) -> None:
    self.cursor.execute("DELETE FROM words WHERE Word=(?)", word)

  def __del__(self):
    del self.cursor
    self.conn.close()


class Sqlobj_for_count_words:

  def __init__(self, file_path: str, conn_type: Conn_type):
    self.file_path = file_path
    self.conn_type = conn_type
    if (os.path.exists(self.file_path)):
      print(f"File : {self.file_path} already exists")
    self.conn = sqlite3.connect(file_path if conn_type == Conn_type.FILE else ':memory:', check_same_thread = False)
    self.cursor = self.conn.cursor()

  def init_def_files(self) -> None:
    # Can add k-words here itself for optimizations but lets keep it that way for now
    try :
      # Metadata to each word
      self.cursor.execute(""" CREATE TABLE word_count (
      WordOne             text,
      WordTwo             text,
      NumberOfTimes       integer,
      RelatedFiles        text
      )""")

    except:
      raise Exception("""TABLE ALREADY INTIALIZED. Delete the
      Sqlobj.init_def_file method or check db file for missing params""")

  def add_single_to_file(self, data : word_count_data) -> None:
    """ADDS SINGLE ELEMENT TO FILE"""
    self.cursor.execute("INSERT INTO word_count VALUES (?, ?, ?, ?)", data)
  def add_multiple_to_file(self, data : list[word_count_data]) -> None:
    """ADDS MULTIPLE ELEMENT TO FILE"""
    self.cursor.executemany("INSERT INTO word_count VALUES (?, ?, ?, ?)", data)

  def update_entity(self, word_one : str, word_two : str, count : int, related_file : str,
                    count_addition : bool = True, rl_file_add_flag : bool = True):
    self.cursor.execute("SELECT NumberOfTimes, RelatedFiles FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                        [word_one], [word_two])
    if (related_file == "" and rl_file_add_flag):
      raise Exception("Relating to an empty file")
    data = self.cursor.fetchone()

    # This check will be slower can improve here
    if (rl_file_add_flag):
      files = data[1].split('|')
      if related_file in files:
        file_add = False
      else:
        file_add = True
    else:
      file_add = False

    if (count_addition == True and file_add):
      self.cursor.execute("UPDATE NumberOfTimes=(?), RelatedFiles=(?) FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                          [data[0]+count], ['|'.join([data[1], related_file])], [word_one], [word_two])
    elif (count_addition == False and file_add):
      self.cursor.execute("UPDATE NumberOfTimes=(?), RelatedFiles=(?) FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                          [count], ['|'.join([data[1], related_file])], [word_one], [word_two])

    elif (count_addition == True and not(file_add)):
      self.cursor.execute("UPDATE NumberOfTimes=(?) FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                          [data[0]+count], [word_one], [word_two])
    else :
      self.cursor.execute("UPDATE NumberOfTimes=(?) FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                          [count], [word_one], [word_two])


  def search_if_word_one_exists(self, query : list[str]) -> bool:
    self.cursor.execute("SELECT COUNT(WordOne) FROM word_count WHERE WordOne=(?)", query)
    k = self.cursor.fetchone()
    if (k[0] == 0):
      return False
    return True

  def search_if_word_two_exists(self, query : list[str]) -> bool:
    self.cursor.execute("SELECT COUNT(WordOne) FROM word_count WHERE WordTwo=(?)", query)
    k = self.cursor.fetchone()
    if (k[0] == 0):
      return False
    return True

  def search_if_instance_exists(self, query_word1 : str, query_word2 : str):
    self.cursor.execute("SELECT COUNT(WordOne) FROM word_count WHERE WordOne=(?) AND WordTwo=(?)",
                        [query_word1, query_word2])
    k = self.cursor.fetchone()
    if (k[0] == 0):
      return False
    return True


  def number_of_word_one_matches(self, query : str):
    self.cursor.execute("SELECT COUNT(WordOne) FROM word_count WHERE WordOne=(?)", query)
    k = self.cursor.fetchone()
    return k[0]

  def number_of_word_two_matches(self, query : str):
    self.cursor.execute("SELECT COUNT(WordOne) FROM word_count WHERE WordTwo=(?)", query)
    k = self.cursor.fetchone()
    return k[0]

  def get_top_contents_of_a_word(self, query : str,
                                  check_if_exists : bool = False,
                                  number_of_words : int = 20):
    if (check_if_exists):
      print(f"Word {query} exists in table is : {search_if_word_one_exists(query)}")

    self.cursor.execute("SELECT * FROM word_count WHERE WordOne=(?) ORDER BY NumberOfTimes DESC",
                        [query])
    data = self.cursor.fetchall()
    return data[:number_of_words]



  def show_all_words(self):
    self.cursor.execute("SELECT * FROM word_count")
    data_all = self.cursor.fetchall()
    for data in data_all:
      print(data)


  # def append_into_exisiting_word(self, word : str, list_of_context_words : list[str],
  #                                count_list_of_words : list[float]) -> None:

  #   # Error check before hand
  #   if len(list_of_context_words) == 0:
  #     raise Exception("Empty list of context words")
  #   if len(count_list_of_words) == 0:
  #     raise Exception("Empty list of context words probabilities")
  #   if len(list_of_context_words) != len(count_list_of_words):
  #     raise Exception("Unequal sizes of word and word prob in consideration")


  #   self.cursor.execute("SELECT ContextWords,ContextWordsProb FROM words WHERE Word=(?)", word)
  #   context_words, context_words_prob = self.cursor.fetchone()
  #
  #   self.cursor.execute("UPDATE words SET ContextWords=(?) WHERE Word=(?)",
  #                       context_words+'|'+'|'.join(list_of_context_words),word)
  #   self.cursor.execute("UPDATE words SET ContextWordsProb=(?) WHERE Word=(?)",
  #                       context_words_prob+'|'+'|'.join(count_list_of_words),word)

  def delete_word(self, word : str) -> None:
    self.cursor.execute("DELETE FROM word_count WHERE Word=(?)", word)

  def __del__(self):
    del self.cursor
    self.conn.close()
