class Repeat:
    def __init__(self, r, rs, re, rc):
        self.r = r
        self.rs = rs
        self.re = re
        self.rc = rc

redundant = Repeat("GTTTTAKATTA(ACTAWRTGG)WATGTAAAK",
                   "GTTTTAKATTAACTAWRTGG",
                   "ACTAWRTGGWATGTAAAK",
                   "GTTTTAKATTAACTAWRTGGWATGTAAAK")

non_redundant_1 = Repeat("GTTTTATATTA(ACTAAGTGG)TATGTAAAG",
                           "GTTTTATATTAACTAAGTGG",
                           "ACTAAGTGG)TATGTAAAG",
                           "GTTTTATATTAACTAAGTGGTATGTAAAG"
                          )

non_redundant_2 = Repeat("GTTTTATATTA(ACTATATGG)AATGTAAAT",
                           "GTTTTATATTAACTATATGG",
                           "ACTATATGGAATGTAAAT",
                           "GTTTTATATTAACTATATGGAATGTAAAT"
                          )

ecoli_r = Repeat("GWGTTCCCC(GCGCCAGCG)GGGATAAACCG",
                   "GWGTTCCCCGCGCCAGCG",
                   "GCGCCAGCGGGGATAAACCG",
                   "GWGTTCCCCGCGCCAGCGGGGATAAACCG")

ecoli_r_1 = Repeat("GWGTTCCCC(GCGCCAGCG)GGGATAAACCG",
                   "GCCAAATAGGGGCGACCGCG",
                   "GCGACCGCGCCCCTTGWG",
                   "GCCAAATAGGGGCGACCGCGCCCCTTGWG")

ecoli_r_2 = Repeat("CGGTTTATCCC(CGCTGGCGC)GGGGAACWC",
                   "CGGTTTATCCCCGCTGGCGC",
                   "CGCTGGCGCGGGGAACWC",
                   "CGGTTTATCCCCGCTGGCGCGGGGAACWC")
