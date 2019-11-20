import requests
from io import BytesIO
from anndata import AnnData, read_h5ad


def _download_adata(url) -> AnnData:
    response = requests.get(url)
    f = BytesIO(response.content)
    return read_h5ad(f)


def pbmc3k() -> AnnData:
    return _download_adata("https://ndownloader.figshare.com/files/18789473?private_link=6e12f5f56bb46842f5ee")


def cite_seq_bone_marrow() -> AnnData:
    return _download_adata("https://ndownloader.figshare.com/files/18788633?private_link=cfbc86f6a399343677ea")


def endoderm_full() -> AnnData:
    return _download_adata("https://ndownloader.figshare.com/files/18789569?private_link=fe99143697ea99121240")


def endoderm_downsampled() -> AnnData:
    return _download_adata("https://ndownloader.figshare.com/files/18788645?private_link=c204122a8d0550282502")
