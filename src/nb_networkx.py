import matplotlib
import networkx

# Doing single graph method for now
def Word_ennumerate(prelist = dict(), word_list = []):
    size = len(prelist)
    for word in word_list:
        if word in prelist:
            continue
        else :
            prelist[word] = size
            size += 1
    return prelist



class Graph:

    def __init__(self, graph_name, initial_nodes = set(), initial_edges = []):
        self.graph_name = graph_name
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(initial_nodes)
        self.graph.add_edges_from(initial_edges)


    def __str__(self):
        return "GRAPH NAME : {0}\n\nNUMBER OF NODES\t: {1}\nNUMBER OF EDGES\t: {2}\n".format(
                self.graph_name, self.graph.number_of_nodes(), self.graph.number_of_edges())


    def add_edges_from(self,edge_list):
        if len(edge_list) == 0 :
            print("Nothing to add")
        else :
            self.graph.add_edges_from(edge_list)


    def show_graph(self):
        networkx.draw(self.graph, with_labels= True, font_size=12, font_weight='bold',
                font_color='black', node_size=0, edge_color='lightgrey', width=0.1, alpha = 0.3)
        matplotlib.pyplot.show()
        matplotlib.pyplot.savefig("Saved.png")
    
    def save_graph(self, file_name = ""):
        if (file_name == ""):
            raise Exception("Please enter valid file name")
        networkx.write_gml(self.graph, f"../saved_graphs/{file_name}.gml")

    def load_graph(self, file_name = ""):
        self.graph = networkx.read_gml(f"../saved_graphs/{file_name}.gml")

    def clear_graph(self):
        self.graph_name = ""
        self.graph.clear()

