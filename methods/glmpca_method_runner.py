import numpy as np
import scanpy as sc
from glmpca.glmpca import glmpca
from ..method_runner import MethodRunner


class GLMPCAMethodRunner(MethodRunner):

    def __init__(self, adata, verbose, n_latent):
        super(MethodRunner, self)
        self.n_latent = n_latent
        self.adata = adata

    def run(self):
        Y = self.adata.X.todense().T
        res = glmpca(Y, self.n_latent)

        # Normalized matrix
        norm = np.dot(res['factors'], res['loadings'].T)
        self.adata.obsm['X_norm'] = norm
        self.adata.obsm['X_emb'] = res['factors']
