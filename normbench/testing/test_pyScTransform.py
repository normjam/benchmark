import numpy as np
from normbench.methods import ad2seurat as a2s
from normbench.methods.data import pbmc3k

def test_pyScTransform():
    adata = pbmc3k()

    a2s.pyScTransform(adata)

    # Test that it runs
    assert 'normalized' in adata.layers

    # Test functionality
    assert np.isclose(adata.layers['normalized'][2,7], 0.69314718)
