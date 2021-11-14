import sqlite3
import os
import enum
# import typing

Case_file_details     = list[str, str, str, str, int, str]
word_data             = list[str, str, str, str]

class Conn_type(enum.Enum):
  FILE    = 0
  MEMORY  = 1


class Sqlobj:

  def __init__(self, file_path: str, conn_type: Conn_type):
    self.file_path = file_path
    self.conn_type = conn_type
    if (os.path.exists(self.file_path)):
        print(f"File : {self.file_path} already exists")
    self.conn = sqlite3.connect(file_path if conn_type == Conn_type.FILE else ':memory:')
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


  def get_all_context_words(self):
    self.cursor.execute("SELECT ContextWords FROM legaldb")
    return self.cursor.fetchall()

  def __del__(self):
    del self.cursor
    self.conn.close()



class SqlObj_for_words:

  def __init__(self, file_path: str, conn_type: Conn_type):
    self.file_path = file_path
    self.conn_type = conn_type
    if (os.path.exists(self.file_path)):
      print(f"File : {self.file_path} already exists")
    self.conn = sqlite3.connect(file_path if conn_type == Conn_type.FILE else ':memory:')
    self.cursor = self.conn.cursor()

  def init_def_file(self) -> None:
    # Can add k-words here itself for optimizations but lets keep it that way for now
    try :
      # Metadata to each word
      self.cursor.execute(""" CREATE TABLE words (
      id                  integer     AUTOINCREMENT,
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

  def search_if_word_exists(self, search_param : str) -> bool:
    self.cursor.execute("SELECT COUNT(Word) FROM words WHERE Word=(?)", search_param)
    k = self.cursor.fetchone()
    if (k[0] == 0):
      return False
    return True

  def append_into_exisiting_word(self, word : str, list_of_context_words : list[str]) -> None:
    if len(list_of_context_words) == 0:
      raise Exception("Empty list of context words")
    self.cursor.execute("SELECT ContextWords FROM words WHERE Word=(?)", word)
    data = self.cursor.fetchone()
    self.cursor.execute("UPDATE words SET ContextWords=(?) WHERE Word=(?)",
                        data+','+','.join(list_of_context_words),word)

  def delete_word(self, word : str) -> None:
    self.cursor.execute("DELETE FROM words WHERE Word=(?)", word)

  def __del__(self):
    del self.cursor
    self.conn.close()
