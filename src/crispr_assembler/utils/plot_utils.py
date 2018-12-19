import numpy as np
import matplotlib.pyplot as plt


def plot_grs(*gr, start=0, end=-1, log = False, all_ticks = False,  s=10):
    f, a = plt.subplots(1, len(gr), figsize=(s,s))

    if end == -1:
        end = gr[0].shape[0]
    if log:
        for i in range(len(gr)): 
            a[i].imshow(np.log(gr[i][start:end,start:end] + 1))
    else:
        for i in range(len(gr)): 
            a[i].imshow(gr[i][start:end,start:end])
            #a[i].colorbar()
#     if all_ticks: 
#         plt.xticks(np.arange(start,end))
#         plt.yticks(np.arange(start,end))
    plt.show()


def plot_gr(gr, save_path, start=0, end=-1, log = False, all_ticks = False, s=10):
    f = plt.figure(figsize=(s,s))
    if end == -1:
        end = gr.shape[0]
    if log:
        plt.imshow(np.log(gr[start:end,start:end] + 1))
    else:
        plt.imshow(gr[start:end,start:end])
    plt.colorbar()
    if all_ticks: 
        plt.xticks(np.arange(start,end))
        plt.yticks(np.arange(start,end))

    f.savefig(save_path)
    #plt.show()
