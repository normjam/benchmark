from scvi.models import VAE
from scvi.inference import UnsupervisedTrainer
from sklearn.preprocessing import LabelEncoder
from scvi.dataset import AnnDatasetFromAnnData


def runScvi(adata, batch, hvg=None):
    # Use non-normalized (count) data for scvi!
    # Expects data only on HVGs

    # checkSanity(adata, batch, hvg)

    # Check for counts data layer
    if 'counts' not in adata.layers:
        raise TypeError('Adata does not contain a `counts` layer in `adata.layers[`counts`]`')

    n_epochs = 100
    n_latent = 10
    n_hidden = 128
    n_layers = 2
    net_adata = adata.copy()
    net_adata.X = adata.layers['counts']
    del net_adata.layers['counts']
    net_adata.raw = None  # Ensure that the raw counts are not accidentally used
    # Define batch indices
    le = LabelEncoder()
    net_adata.obs['batch_indices'] = le.fit_transform(net_adata.obs[batch].values)
    net_adata = AnnDatasetFromAnnData(net_adata)
    vae = VAE(
        net_adata.nb_genes,
        reconstruction_loss='nb',
        n_batch=net_adata.n_batches,
        n_layers=n_layers,
        n_latent=n_latent,
        n_hidden=n_hidden,
    )
    trainer = UnsupervisedTrainer(
        vae,
        net_adata,
        train_size=1,
        use_cuda=False,
    )
    trainer.train(n_epochs=n_epochs, lr=1e-3)
    full = trainer.create_posterior(trainer.model, net_adata, indices=np.arange(len(net_adata)))
    latent, _, _ = full.sequential().get_latent()
    adata.obsm['X_emb'] = latent
    return adata
