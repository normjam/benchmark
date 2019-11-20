import numpy as np
from glmpca.glmpca import glmpca

from methods.method_runner import MethodRunner


class GLMPCAMethodRunner(MethodRunner):

    def __init__(self, data, verbose, n_latent=10, likelihood="poi"):
        """
        Contains parameters for running GLMPCA normalization. n_latent is the number of latent dimensions and the
        likelihood is the likelihood function to use. Likelihood should generally be one of "poi" which represents
        Poisson or "nb" which represents negative binomial.
        """

        MethodRunner.__init__(self, data, verbose)
        self.n_latent = n_latent
        self.likelihood = likelihood

    def run(self):
        Y = self.data.X.todense().T
        res = glmpca(Y, self.n_latent, fam=self.likelihood)

        # Normalized matrix
        norm = np.dot(res['factors'], res['loadings'].T)
        self.data.obsm['X_norm'] = norm
        self.data.obsm['X_emb'] = res['factors']

        self.dump_to_loom(f"glmpca_normalized_{self.likelihood}", norm, {}, {})
        self.dump_to_loom(f"glmpca_latent_{self.likelihood}", res['factors'], {}, {})
