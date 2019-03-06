import numpy as np
import pickle
import tqdm
from multiprocessing import Pool

class EmbeddingsCalculator:
    def __init__(self):
        self.embeddings = None

    def fit(self, graph):
        self.embeddings = self.build_embeddings(graph)

    def get_embeddings(self):
        return self.embeddings

    def make_argsorts(self, gr):
        self.argsort_gr_i = np.zeros_like(gr)
        self.argsort_gr_j = np.zeros_like(gr)

        for i in range(gr.shape[0]):
            self.argsort_gr_i[i] = np.argsort(gr[i])
            self.argsort_gr_j[:, i] = np.argsort(gr[:, i])

    def build_embeddings(self, graph, njobs=8, function_set=None):
        if njobs > 1:
            p = Pool(njobs)
            inp = []
            for i in range(graph.shape[0]):
                for j in range(graph.shape[1]):
                    inp.append([graph, i, j])
            embs = p.map(self.get_vertex_emb,inp)
        else:
            embs = []
            for i in tqdm.tqdm(range(graph.shape[0])):
                for j in range(graph.shape[1]):
                    embs.append(self.get_vertex_emb(graph, i, j))

        return np.stack(embs)

    def get_vertex_emb(self, arg):
        gr, i, j = arg
        emb = []
        emb.extend(self.get_percentiles_fast(gr, i, j))
        emb.extend(self.get_ratios(gr, i, j))
        emb.extend(self.get_median_ratios_fast(gr, i, j))

        return np.array(emb)

    def get_percentiles(self, gr, i, j):
        return [np.where(np.argsort(gr[i]) == j)[0][0] / (gr.shape[0] - 1),
                np.where(np.argsort(gr[:, j]) == i)[0][0] / (gr.shape[0] - 1)]

    def get_percentiles_fast(self, gr, i, j):
        return [np.where(self.argsort_gr_i[i] == j)[0][0] / (gr.shape[0] - 1),
                np.where(self.argsort_gr_j[:, j] == i)[0][0] / (gr.shape[0] - 1)]

    def get_ratios(self, gr, i, j):
        return [gr[i, j] / max(1, gr[i].sum()), gr[i, j] / max(1, gr[:, j].sum())]

    def get_median_ratios(self, gr, i, j):
        return [np.log(gr[i, j] / max(1, np.median(gr[i])) + 1), np.log(gr[i, j] / max(1, np.median(gr[:, j])) + 1)]

    def get_median_ratios_fast(self, gr, i, j):
        return [np.log(gr[i, j] / max(1, gr[i][self.argsort_gr_i[i][gr.shape[0] // 2]]) + 1),
                       np.log(gr[i, j] / max(1, gr[:, j][self.argsort_gr_j[:, j]][gr.shape[0] // 2]) + 1)]

    def _build_old_style_embedding(self, graph, i, j):
        '''
        This embedding builder builds the following embeddings:
        read weight / all outgoing for first vertex
        read weight / all incoming for second vertex
        read weight / all outgoing for second vertex
        read weight / all incoming for first vertex
        '''

        # embedding = np.empty(self.embedding_shape)
        #
        # embedding[0] = graph[i,j] / graph[i].sum()
        # embedding[1] = graph[i,j] / graph[:, j].sum()
        # embedding[2] = graph[i,j] / graph[j].sum()
        # embedding[3] = graph[i,j] / graph[:, i].sum()
        #
        # return embedding
        pass

    # def load_model(self, model_name):
    #     pickle.load()
