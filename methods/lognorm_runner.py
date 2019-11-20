import scanpy as sc

from methods.method_runner import MethodRunner


class LogNormalizationRunner(MethodRunner):

    def __init__(self, data, verbose):
        MethodRunner.__init__(self, data, verbose)

    def run(self):
        sc.pp.normalize_per_cell(self.data, copy=True)
        sc.pp.log1p(self.data)

        # Normalized matrix
        self.dump_to_h5ad("lognorm_normalized")
