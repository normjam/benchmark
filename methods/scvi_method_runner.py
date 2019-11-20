import anndata
import numpy as np
from scvi.dataset import AnnDatasetFromAnnData
from scvi.inference import UnsupervisedTrainer
from scvi.models import VAE
from sklearn.preprocessing import LabelEncoder

from ..method_runner import MethodRunner


class ScViMethodRunner(MethodRunner):

    def __init__(self, data, verbose, batch, highly_variable_genes):
        super(MethodRunner, self)
        self.batch = batch
        self.highly_variable_genes = highly_variable_genes

        self.validate_method_parameters(self.data, self.batch)

    def run(self):
        n_epochs = 100
        n_latent = 10
        n_hidden = 128
        n_layers = 2
        net_data = self.data.copy()
        net_data.X = self.data.layers['counts']
        del net_data.layers['counts']
        net_data.raw = None  # Ensure that the raw counts are not accidentally used

        # Define batch indices
        le = LabelEncoder()
        net_data.obs['batch_indices'] = le.fit_transform(net_data.obs[self.batch].values)
        net_data = AnnDatasetFromAnnData(net_data)
        vae = VAE(net_data.nb_genes, reconstruction_loss='nb', n_batch=net_data.n_batches, n_layers=n_layers,
                  n_latent=n_latent, n_hidden=n_hidden)
        trainer = UnsupervisedTrainer(vae, net_data, train_size=1, use_cuda=False)
        trainer.train(n_epochs=n_epochs, lr=1e-3)
        full = trainer.create_posterior(trainer.model, net_data, indices=np.arange(len(net_data)))
        latent, _, _ = full.sequential().get_latent()
        self.data.obsm['X_emb'] = latent

    def validate_method_parameters(self):
        """
        Checks the input parameters for the scVI Method Runner and raises an exception if it fails a basic set of
        sanity check around typing.
        """

        # Validate data
        if type(self.data) is not anndata.AnnData:
            raise TypeError("Input data is not a valid AnnData object")
        if 'counts' not in self.data.layers:
            raise TypeError("Input data does not contain a `counts` layer in `data.layers[`counts`]`")

        # Validate batch
        obs = self.data.obs
        if self.batch not in obs:
            raise ValueError(f"Column {self.batch} is not in obs")
        elif self.verbose:
            print(f"Object contains {obs[self.batch].nunique()} batches.")

        # Validate highly variable genes
        if self.highly_variable_genes:
            if type(self.highly_variable_genes) is not list:
                raise TypeError("HVG list is not a list")
            else:
                data_var = self.data.var
                if not all(i in data_var.index for i in self.highly_variable_genes):
                    raise ValueError("Not all HVGs are in the data object")
