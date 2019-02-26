from crispr_assembler.utils.utils import rc as rev_compl


class Repeat:
    def __init__(self, r, rs, re, rc):
        self.r = r
        self.rs = rs
        self.re = re
        self.rc = rc

    def complementary(self):
        complementary = Repeat(r=rev_compl(self.r),
                               rs=rev_compl(self.rs),
                               re=rev_compl(self.re),
                               rc=rev_compl(self.rc))

        return complementary

    def reverse(self):
        reverse = Repeat(r=self.r[::-1],
                         rs=self.re[::-1],
                         re=self.rs[::-1],
                         rc=self.rc[::-1])

        return reverse

    def reverse_complementary(self):
        return self.reverse().complementary()


redundant = Repeat("GTTTTAKATTA(ACTAWRTGG)WATGTAAAK",
                   "GTTTTAKATTAACTAWRTGG",
                   "ACTAWRTGGWATGTAAAK",
                   "GTTTTAKATTAACTAWRTGGWATGTAAAK")

redundant_2 = Repeat("GTTTTAKATTA(ACTAWRTGG)WATGTAAAK",
                   "GTTTTAKATTAACTAWRTGG",
                   "ACTAWRTGGWATGTAAAK",
                   "GTTTTAKATTAACTAWRTGGWATGTAAAK")

#cdif = Repeat("ATTTACATTCCATATAGTTAATCTAAAAC")

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
