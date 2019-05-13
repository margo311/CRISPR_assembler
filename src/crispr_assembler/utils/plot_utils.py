import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_grs(*gr, start=0, end=-1, log = False, all_ticks = False,  s=10, subplots_form=None):
    if subplots_form is None:
        subplots_form = (1, len(gr))

    f, a = plt.subplots(*subplots_form, figsize=(s,s))

    a = a.flatten()
    if end == -1:
        end = gr[0].shape[0]
    if log:
        for i in range(len(gr)): 
            #a[i // subplots_form[0]][i % subplots_form[0]].imshow(- np.log(gr[i][start:end,start:end] + 1), cmap='gray')
            a[i].imshow(np.log(gr[i][start:end,start:end] + 1)) #, cmap='PiYG')
    else:
        for i in range(len(gr)): 
            #a[i // subplots_form[0]][i % subplots_form[0]].imshow(- gr[i][start:end,start:end], cmap='gray')
            a[i].imshow(gr[i][start:end,start:end])#, cmap='gray')
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
            s=None,
            idx_to_sp=None):

    if s is None:
        s = int(gr.shape[0] * 0.2)

    f = plt.figure(figsize=(s,s+2))
    plt.gcf().subplots_adjust(bottom=0.40, left = 0.40)
    ax = plt.gca()
    if end == -1:
        end = gr.shape[0]
    if log:
        im = ax.imshow(np.log(gr[start:end,start:end] + 1))#, cmap='gray')
    else:
        im = ax.imshow(gr[start:end,start:end])#, cmap='gray')



    if all_ticks or idx_to_sp is not None:
        if idx_to_sp is not None:
            fill = [idx_to_sp[i] for i in np.arange(start, end)]
        else:
            fill = np.arange(start, end)
        plt.xticks(np.arange(start,end), fill, rotation = 90, fontsize=s)
        plt.yticks(np.arange(start,end), fill, fontsize=s)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    cax.tick_params(labelsize=s)
    plt.colorbar(im, cax=cax)

    if save_path is not None:
        f.savefig(save_path)

