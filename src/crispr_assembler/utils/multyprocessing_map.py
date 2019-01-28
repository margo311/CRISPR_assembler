from multiprocessing import Pool


def mp_map(func, l, workers=4):
    p = Pool(workers)

    return p.map(func, l)