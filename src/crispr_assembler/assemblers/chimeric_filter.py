import pickle


class ChimericFilter:
    def __init__(self, model_path=None, model=None):
        if model_path is None:
            model_path = "../datastyle/pretrained_filters/gb_rep_to_rep_0"

        self.filter = pickle.load(open(model_path, 'rb'))

    def filter_graph(self, graph, embeddings = None):
        return self.filter.predict(embeddings).reshape(graph.shape)




