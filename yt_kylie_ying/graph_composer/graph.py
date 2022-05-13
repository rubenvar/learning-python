# the Markov Chain representation
import random


class Vertex:
    def __init__(self, value):  # value will be the word
        self.value = value
        self.adjacent = {}  # nodes that have an edge from this vertex
        self.neighbors = []
        self.neighbors_weights = []

    def add_edge_to(self, vertex, weight=0):
        # add an adge to the vertex with some weight (0 by default)
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        # increment the value of the edge if it exists
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weights.append(weight)

    def next_word(self):
        # randomly select next word based on weights
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]


class Graph:
    # put the vertex together in a graph
    def __init__(self):
        self.vertices = {}

    def get_vertex_values(self):
        # all the words encountered so far
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            # if value not in graph
            self.add_vertex(value)
        return self.vertices[value]  # get the vertex object

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()
