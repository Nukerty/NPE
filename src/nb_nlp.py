import nltk
import NNP_extractor as npe
# import nlp
# import itertools
import os
import datetime

stop_words = set(nltk.corpus.stopwords.words('english'))

class Folder:
    """
    FOLDER ACCESS CLASS : has properties
    1) check_dir - to find correctly annotated files from the documents
    """
    def __init__(self,folder_path : str):
        self.folder_path = folder_path
        self.correct_files = []

    def check_dir(self):
        files = os.listdir(self.folder_path)
        for file in files:
            # nb_nlp.load_file_path("../.data/" + file)
            with open (self.folder_path+file) as f:
                data = f.read().split('\n')
                # print(f"FILE NAME : {file}")
                if (data[6].find('1') == 0):
                    # print(1)
                    if (len(data[2]) == 0):
                        #print(2)
                        if (data[5].find("The Judgement") == 0 or
                        data[5].find("The Judgment") == 0 ):
                            # print(3)
                            try:
                                if (time.strptime(data[3], "%d %B %Y")):
                                    self.correct_files.append(file)
                            except:
                                continue


    class File :
        """
        FILE ACCESS CLASS : 
        1)  __str__     : print main points
        2) read_file    : read a file
        3) parse_file   : obtain data from the file
        """
        def __init__(self, folder_path : str, file_name : str):
            self.folder_path : str = folder_path
            self.file_name : str = file_name
            self.data : str = ""
            self.parties_involved: list[str, str] = ["",""]
            self.court_of_appeal : str = ""
            self.date_of_judgement = datetime.datetime.fromisoformat('1950-01-01')
            self.judge_involved : str = ""
            self.text : str = ""
            self.noun_words : set = set()
            # self.appeal_type = ""
            # self.appeal_no = ""

        def read_file(self):
            with open (self.folder_path + self.file_name) as f :
                self.data = f.read()

        def parse_file(self):
            if self.data != "" :
                self.lines = self.data.split('\n')
                self.parties_involved = self.lines[0].split(' v ')
                self.court_of_appeal = self.lines[1]
                self.date_of_judgement = datetime.datetime.strptime(self.lines[3], "%d %B %Y")
                self.judge_involved = self.lines[5].split(': ')[1]
                for line in self.lines[6:] :
                    if len(line) > 0 :
                        # 5 might be better
                        if line[:6].find('.') > 0:
                            line = line[line[:6].find('.')+1:]
                        sentences = nltk.sent_tokenize(line)
                        for sentence in sentences :
                            NNP_list = npe.start(sentence)
                            _ = [self.noun_words.add(x) for x in NNP_list]
                self.data = ""
                self.lines = ""
            else :
                raise Exception("Please load in file")


        def show_nwds(self, show_words : bool = False) -> None:
            if (show_words):
                _ = [print(x, end='|') for x in self.noun_words]
            print(f"\n{len(self.noun_words)}")

        def get_nwds_as_str(self) -> str:
            # Changed ',' variant to '|' because of less use
            return '|'.join(self.noun_words)

        def __str__ (self):
            return "Parties involved : {0} vs. {1}\nCourt of Appeal : {2}\nDate of Judgement : {3}\nNo. of words in file : {4}".format(
                self.parties_involved[0], self.parties_involved[1], 
                self.court_of_appeal, time.strftime("%d-%M-%Y", self.date_of_judgement), 
                len(self.noun_words))





class word :
    # newid = itertools.count()
    def __init__(self, name : str, definition :str ="",
                 connected_words: list[str] = [], contextwordsprob : list[float] = [],
                 related_files: list[str] = []):
        self.name = name
        # self.definition = definition
        self.contextwords = connected_words
        self.contextwordsprob = contextwordsprob
        self.related_files = related_files
        # self.id = word.newid()

    def __str__(self):
        # Shows the top 5 files
        return "Word : {0:-20}\nDefinition :{1:-100}\nRelated files : {2}\n".format(
            self.name, self.definition, self.related_files[:5])

    def add_context_words(self, add_context_words : set[str],
                          probability_list : list[float], related_files : list[str]):
        for i in range (len(add_context_words)):

            if (add_context_words[i] in self.contextwords):
                contextwordsprob[self.contextwords.index(add_context_words[i])] += probability_list
                continue

            self.contextwords.append(add_context_words[i])
            self.contextwordsprob.append(probability_list[i])

        for rl_file in related_files:
            if (rl_file in self.related_files):
                continue
            self.related_files.append(rl_file)

    def __del__(self):
        self.name = ""
        self.context_words = []
        self.contextwordsprob = []
        self.related_files = []



    # def __add__(self, w1, w2):
    #     if (w1.name == w2.name) :
    #         if (len(w1.connected_words) > len(w2.connected_words)) :
    #             for word in w2.connected_words:
    #                 if ()
    #     else :
    #         raise Exception("Not the same words")

class Graph_of_Words:

    # newid = itertools.count().next
    def __init__(self, name : str, words : list[str] = []):
        if (name != "") :
            self.name = name
            self.words = words

    def __str__(self) :
        return "Graph Name : {0}\nGraph Words : {1}".format(self.name, self.words)

    def __len__(self):
        return len(self.words)

    def __cointains__(self, word):
        return (word in self.words)

    # # How do you add two Graphs then?
    # def __add__ :


# Sample txt file
# def load_file_path(file_path="../.data/1979_A_20.txt"):
#     x = File(file_path)
#     x.read_file()
#     x.parse_file()
#     print(file_path)
#     del x
