
runBASiCS<-function(Seurat_Obj)
{
  library(BASiCS)
  umiData<-Seurat_Obj@assays$RNA@counts
  umiData <- SingleCellExperiment::SingleCellExperiment(assays = list('counts' = umiData))
  
  # naive test of BASiCS, no batches, no clustering information, data are expected to be filtered with some QC
  Chain <- BASiCS_MCMC(Data = umiData, N = 1000, Thin = 10, Burn = 500, 
                       WithSpikes = FALSE,
                       PrintProgress = FALSE, Regression = TRUE)
  
  DenoisedCounts <- BASiCS_DenoisedCounts(Data = umiData, Chain = Chain)
  str(DenoisedCounts)
  write.table(DenoisedCounts, "BASiCS_NormalizedCounts.tsv", sep = "\t")
   return(DenoisedCounts)
}