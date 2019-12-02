import requests
from io import BytesIO
from anndata import AnnData, read_h5ad
import numpy as np


def _download_adata(url) -> AnnData:
    response = requests.get(url)
    f = BytesIO(response.content)
    return read_h5ad(f)


# Just cast unsigned ints to int64
# Hope that this doesn't break (uint64)
def _no_unsigned_int(pdata):
    for i,t in enumerate(pdata.dtypes):
        if t.name.startswith('u'): #this is an unsigned integer
            colname = pdata.columns[i]
            pdata[colname] = pdata[colname].astype(int)


# Helper function to clean anndata object
def clean_adata(adata) -> AnnData:
    _no_unsigned_int(adata.var)
    _no_unsigned_int(adata.obs)
    return(adata)
    
def pbmc3k() -> AnnData:
    return clean_adata(_download_adata("https://ndownloader.figshare.com/files/18789473?private_link=6e12f5f56bb46842f5ee"))


def cite_seq_bone_marrow() -> AnnData:
    return clean_adata(_download_adata("https://ndownloader.figshare.com/files/18788633?private_link=cfbc86f6a399343677ea"))


def endoderm_full() -> AnnData:
    return clean_adata(_download_adata("https://ndownloader.figshare.com/files/18789569?private_link=fe99143697ea99121240"))


def endoderm_downsampled() -> AnnData:
    return clean_adata(_download_adata("https://ndownloader.figshare.com/files/18788645?private_link=c204122a8d0550282502"))


