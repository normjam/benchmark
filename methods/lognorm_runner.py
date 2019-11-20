import scanpy as sc

from ..method_runner import MethodRunner


class LogNormalizationRunner(MethodRunner):

    def __init__(self, data, verbose):
        super(MethodRunner, self)

    def run(self):
        sc.pp.normalize_per_cell(self.data)
        sc.pp.log1p(self.data)

        # Normalized matrix
        self.dump_to_loom("lognorm_normalized", self.data.X, {}, {})
