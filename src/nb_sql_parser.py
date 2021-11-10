import sqlite3
import os
import enum
# import typing

Case_file_details = list[str, str, str, str, int, str]
word_data = list[str, str, str, str]

class Conn_type(enum.Enum):
    FILE = 0
    MEMORY = 1


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
        self.conn.commit()

    def read_all_entries(self):
        self.cursor.execute("SELECT * FROM legaldb")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)


    def get_all_context_words(self):
        self.cursor.execute("SELECT * FROM legaldb")
        rows = self.cursor.fetchall()
        for row in rows:
            pass


    def init_def_file_words(self) -> None:
        # Can add k-words here itself for optimizations but lets keep it that way for now
        try :
            self.cursor.execute(""" CREATE TABLE words (
            Word                text,
            ContextWords        text,
            ContextWordsProb    text,
            RelatedFiles        text
            )""")

        except:
            raise Exception("""TABLE ALREADY INTIALIZED. Delete the
            Sqlobj.init_def_file method or check db file for missing params""")

    def add_single_to_file_words(self, data : word_data) -> None:
        """ADDS SINGLE ELEMENT TO FILE"""
        self.cursor.execute("INSERT INTO words VALUES (?, ?, ?, ?)", data)
    def add_multiple_to_file_words(self, data : list[word_data]) -> None:
        """ADDS MULTIPLE ELEMENT TO FILE"""
        self.cursor.executemany("INSERT INTO words VALUES (?, ?, ?, ?)", data)

    def __del__(self):
        del self.cursor
        self.conn.close()
