
runSCNorm<-function(Seurat_Obj)
{
  library(SCnorm)
  library(Seurat)
  Conditions = Idents(Seurat_Obj)
  umiData <- SingleCellExperiment::SingleCellExperiment(assays = list('counts' = Seurat_Obj@assays$RNA@counts))
  
  str(umiData)
  head(Conditions)
  
  # pdf("check_exampleData_count-depth_evaluation.pdf", height=5, width=7)
  # countDeptEst <- plotCountDepth(Data = umiData, Conditions = Conditions,
  #                                FilterCellProportion = .1, NCores=1)
  # dev.off()
  # str(countDeptEst)
  # head(countDeptEst[[1]])
  
  DataNorm <- SCnorm(Data = umiData, 
                     Conditions= Conditions,
                     PrintProgressPlots = TRUE,
                     FilterCellNum = 10,
                     PropToUse = .1,
                     Thresh = .1,
                     ditherCounts = TRUE)
  
  str(DataNorm@assays@data$counts)
  str(DataNorm@assays@data$normcounts)

  write.table(DataNorm@assays@data$normcounts, "NormalizedCounts.tsv", sep = "\t")
  #NormSeurat_Obj<-CreateSeurat_Obj(raw.data = Matrix(DataNorm@assays@data$normcounts), project = "test")
  return(DataNorm@assays@data$normcounts)
  # Seurat has convert function, use it
  # #this did not work, requires Seurat re-intallation ...
  # NormSeurat_Obj<-CreateSeurat_Obj(raw.data = Matrix(DataNorm@assays@data$normcounts), project = "test")
  # pfile <- Convert(from = NormSeurat_Obj, to = "loom", filename = "NormCounts.loom", 
  #                  display.progress = FALSE)
  # pfile
  
}
