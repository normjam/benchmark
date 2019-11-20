import anndata2ri
import rpy2.robjects as ro
import scanpy as sc
from scipy.sparse import issparse


class ScTransformMethodRunner(MethodRunner):
    def __init__(self, data, verbose):
        MethodRunner.__init__(self, data, verbose)

    def run(self):
        """
        Function to call scTransform from Python
        """

        ro.r('library(Seurat)')
        ro.r('library(scater)')
        anndata2ri.activate()

        sc.pp.filter_genes(self.data, min_cells=5)

        if issparse(self.data.X):
            if not self.data.X.has_sorted_indices:
                self.data.X.sort_indices()

        for key in self.data.layers:
            if issparse(self.data.layers[key]):
                if not self.data.layers[key].has_sorted_indices:
                    self.data.layers[key].sort_indices()

        ro.globalenv['adata'] = self.data

        ro.r('seurat_obj = as.Seurat(adata, counts="X", data = NULL)')

        ro.r('res <- SCTransform(object=seurat_obj)')

        norm_x = ro.r('res@assays$SCT@data').T

        self.data.layers['normalized'] = norm_x

        self.dump_to_h5ad("scTransform")
