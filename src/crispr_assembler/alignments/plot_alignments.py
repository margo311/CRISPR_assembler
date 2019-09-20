import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def draw_array(ax, array, cmap, x0, y0, step = 0.`04):
    rectangles = []
    for i, a in enumerate(array):
        if a == '-':
            color = 'none'
        else:
            color = 'g'#cmap(a*16 % cmap.N)
        rectangles.append(Rectangle((x0 + i * step*2, y0), step*2, step,linewidth=1,
                                    edgecolor='black',
                                    facecolor=color,
                                    alpha = 1))

    for r in rectangles:
        ax.add_patch(r)
    return rectangles #rectangles


def draw_array_triangles(ax, array, cmap, x0, y0, mask=None, step=0.04):
    rectangles = []
    for i, a in enumerate(array):
        if not mask is None:
            if mask[i] == 0:
                color = 'none'
            elif mask[i] == 1:
                color = 'g'
            elif mask[i] == 2:
                color = 'y'
        else:
            if a == '-':
                color = 'none'
            else:
                color = cmap(3)

        if a != "-":
            rectangles.append(plt.Polygon([[x0 + i * step * 2, y0],
                                           [x0 + (i + 1) * step * 2, y0],
                                           [x0 + i * step * 2 + step, y0 + step * 1.1]],
                                          # edgecolor='black',
                                          facecolor=color,
                                          alpha=0.5))
        else:
            rectangles.append(Rectangle((x0 + i * step * 2, y0), step * 2, step, linewidth=1,
                                        edgecolor='black',
                                        facecolor='none',
                                        alpha=0.2))

        plt.text(x0 + i * step * 2, y0, a)

    for r in rectangles:
        ax.add_patch(r)
    return rectangles  # rectangles


def draw_alignment(ax, seq, targets, base_key, keys, cmap, x0, y0, step=0.04):
    rectangles = draw_array(ax, seq, cmap, x0, y0)
    plt.text(x0 - 10 * step, y0, base_key)

    # plt.show()
    i = 0
    for i, t in enumerate(targets[1:]):
        mask = []
        for j in range(len(seq)):
            if seq[j] == t[j] and seq[j] == '-':
                mask.append(0)
            elif seq[j] == t[j]:
                mask.append(1)
            else:
                mask.append(2)

        rectangles = draw_array_triangles(ax, t, cmap, x0, y0 - (i + 1) * step, mask)
        plt.text(x0 - 10 * step, y0 - (i + 1) * step, keys[i + 1])
    #         else:
    #             rectangles = draw_array(ax, t,cmap, y0 - (i+1) * step)
    return y0 - (i + 2) * step