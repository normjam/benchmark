import scanpy as sc
from scipy.sparse import issparse


def pyScTransform(adata, output_file=None):
    """
    Function to call scTransform from Python
    """
    import rpy2.robjects as ro
    import anndata2ri

    ro.r('library(Seurat)')
    ro.r('library(scater)')
    anndata2ri.activate()

    sc.pp.filter_genes(adata, min_cells=5)
    
    if issparse(adata.X):
        if not adata.X.has_sorted_indices:
            adata.X.sort_indices()

    for key in adata.layers:
        if issparse(adata.layers[key]):
            if not adata.layers[key].has_sorted_indices:
                adata.layers[key].sort_indices()

    ro.globalenv['adata'] = adata

    ro.r('seurat_obj = as.Seurat(adata, counts="X", data = NULL)')

    ro.r('res <- SCTransform(object=seurat_obj, return.only.var.genes = FALSE, do.correct.umi = FALSE)')

    norm_x = ro.r('res@assays$SCT@scale.data').T

    adata.layers['normalized'] = norm_x

    if output_file:
        adata.write(output_file)
