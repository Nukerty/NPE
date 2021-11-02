import nltk
import nlp
import itertools
import time


class File :
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = ""
        self.parties_involved = ["",""]
        self.court_of_appeal = ""
        self.date_of_judgement = ""
        # self.appeal_type = ""
        # self.appeal_no = ""

    def read_file(self):
        with open (self.file_name) as f :
            self.data = f.read()

    def parse_file(self):
        if self.data != "" :
            self.lines = self.data.split('\n')
            self.parties_involved = self.lines[0].split(' v ')
            self.court_of_appeal = self.lines[1]
            self.date_of_judgement = time.strptime(self.lines[3], "%d %B %Y")
            self.data = ""
            self.lines = ""
        else :
            raise Exception("Please load in file")

    def __str__ (self):
        return "Parties involved : {0} vs. {1}\nCourt of Appeal : {2}\nDate of Judgement : {3}".format(
            self.parties_involved[0], self.parties_involved[1], self.court_of_appeal, self.date_of_judgement)


class word :

    # newid = itertools.count()
    def __init__(self, name, defintion="", connected_words=[]):
        self.name = name
        self.definition = definition
        self.connected_words = connected_words
        # self.id = word.newid()

    def __str__(self):
        return "(Word : {0:-20}\tDefinition :{1:-100})".format(self.name, self.defintion)

    # def __add__(self, w1, w2):
    #     if (w1.name == w2.name) :
    #         if (len(w1.connected_words) > len(w2.connected_words)) :
    #             for word in w2.connected_words:
    #                 if ()
    #     else :
    #         raise Exception("Not the same words")




class Graph_of_Words:

    # newid = itertools.count().next

    def __init__(self, name, words = []):
        if (name != "") :
            self.name = name
            self.words = words

    def __str__(self) :
        return "Graph Name : {0}\nGraph Words : {1}".format(name, words)

    def __len__(self):
        return len(self.words)

    def __cointains__(self, word):
        return (word in self.words)

    # # How do you add two Graphs then?
    # def __add__ :


# Sample txt file
def load_file_path(file_path="../.data/1979_A_20.txt"):
    x = File(file_path)
    x.read_file()
    x.parse_file()
    print(file_path)
    del x




