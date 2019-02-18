
quality_symbols1 = r'!"#$%&'
quality_symbols2 = "'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

quality_dict = {}
quality_dict_r = {}
for i, char in enumerate(quality_symbols1 + quality_symbols2):
    quality_dict[char] = i
    quality_dict_r[i] = char


def get_quality(x):
    return quality_dict[x]


def get_lowest_q(array, gq = get_quality):
    return quality_dict[min(array, key=gq)]