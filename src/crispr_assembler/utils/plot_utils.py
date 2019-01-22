import numpy as np
import matplotlib.pyplot as plt


def plot_grs(*gr, start=0, end=-1, log = False, all_ticks = False,  s=10):
    f, a = plt.subplots(1, len(gr), figsize=(s,s))

    if end == -1:
        end = gr[0].shape[0]
    if log:
        for i in range(len(gr)): 
            a[i].imshow(- np.log(gr[i][start:end,start:end] + 1), cmap='gray')
    else:
        for i in range(len(gr)): 
            a[i].imshow(- gr[i][start:end,start:end], cmap='gray')
            #a[i].colorbar()
#     if all_ticks: 
#         plt.xticks(np.arange(start,end))
#         plt.yticks(np.arange(start,end))
    plt.show()


def plot_gr(gr,
            save_path=None,
            start=0,
            end=-1,
            log = False,
            all_ticks = False,
            s=10,
            idx_to_sp=None):

    f = plt.figure(figsize=(s,s+2))
    plt.gcf().subplots_adjust(bottom=0.40, left = 0.40 )
    if end == -1:
        end = gr.shape[0]
    if log:
        plt.imshow(np.log(gr[start:end,start:end] + 1), cmap='gray')
    else:
        plt.imshow(gr[start:end,start:end], cmap='gray')
    plt.colorbar()
    if all_ticks or idx_to_sp is not None:
        if idx_to_sp is not None:
            fill = [idx_to_sp[i] for i in np.arange(start, end)]
        else:
            fill = np.arange(start, end)
        plt.xticks(np.arange(start,end), fill, rotation = 90)
        plt.yticks(np.arange(start,end), fill)

    if save_path is not None:
        f.savefig(save_path)

