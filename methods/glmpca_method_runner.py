import numpy as np
from glmpca.glmpca import glmpca

from ..method_runner import MethodRunner


class GLMPCAMethodRunner(MethodRunner):

    def __init__(self, data, verbose, n_latent):
        super(MethodRunner, self)
        self.n_latent = n_latent

    def run(self):
        Y = self.data.X.todense().T
        res = glmpca(Y, self.n_latent)

        # Normalized matrix
        norm = np.dot(res['factors'], res['loadings'].T)
        self.adata.obsm['X_norm'] = norm
        self.adata.obsm['X_emb'] = res['factors']

        self.dump_to_loom("glmpca_normalized", norm, {}, {})
        self.dump_to_loom("glmpca_latent", res['factors'], {}, {})
