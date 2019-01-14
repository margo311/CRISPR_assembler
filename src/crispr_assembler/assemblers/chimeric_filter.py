import numpy as np
import pickle

class ChimericFilter:
    def __init__(self, model_name=None, model=None):
        if not model is None:
            self.model = model
        elif not model_name is None:
            self.model = self.load_model(model_name)
        else:
            raise Exception("Either model or model_name should be specified if you'd like to filter smth")

        self.embedding_shape = 4

    def filter_graph(self, graph):
        embeddings = self.build_embeddings(graph)
        predictions = self.model.predict(embeddings)
        return predictions.reshape(graph.shape)

    def build_embeddings(self, graph):
        embeddings = np.empty((graph.shape[0], graph.shape[1], self.embedding_shape))

        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]):
                embeddings[i,j] = self.build_single_embedding(graph, i, j)

        return embeddings

    def build_single_embedding(self, graph, i, j):
        '''
        This embedding builder builds the following embeddings:
        read weight / all outgoing for first vertex
        read weight / all incoming for second vertex
        read weight / all outgoing for second vertex
        read weight / all incoming for first vertex
        '''

        embedding = np.empty(self.embedding_shape)

        embedding[0] = graph[i,j] / graph[i].sum()
        embedding[1] = graph[i,j] / graph[:, j].sum()
        embedding[2] = graph[i,j] / graph[j].sum()
        embedding[3] = graph[i,j] / graph[:, i].sum()

        return embedding

    def load_model(self, model_name):
        pickle.load()
