import sys
#from crispr_assembler.utils.multyprocessing_map import mp_map
from multiprocessing import Pool


class FastqProcessor:
    def __init__(self, process_function, source=sys.stdin):
        self.process_function = process_function
        self.source = source

    def process(self):
        buffer = []
        for line_idx, line in enumerate(self.source):
            if len(buffer) < 4:
                buffer.append(line)
            if len(buffer) == 4:
                position, read, plus, quality = buffer
                buffer = []
                yield self.process_function(position, read, plus, quality)

    def process_by_batch(self, pool, batch_size=1, drop_last=False):
        buffer = []
        batch = []

        for line_idx, line in enumerate(self.source):
            if len(batch) < batch_size:
                if len(buffer) < 4:
                    buffer.append(line)
                if len(buffer) == 4:
                    batch.append(buffer)
                    buffer = []

            if len(batch) == batch_size:
                batch_copy = [x for x in batch]
                batch = []
                yield list(pool.map(self.wrap_function, batch_copy))

        yield list(pool.map(self.wrap_function, batch))

    def wrap_function(self, sample):
        return self.process_function(*sample)