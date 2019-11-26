install.packages("Seurat")
install.packages("devtools")

library("devtools")
install.packages(c("RcppEigen", "urltools", "Rtsne","BiocManager","robustbase"))

BiocManager::install(
  c("GO.db", "org.Hs.eg.db","org.Mm.eg.db", "pcaMethods", "DESeq2", "edgeR", "BiocGenerics", "SCnorm", "BASiCS"),
  version = "3.10",
  update = TRUE,
  ask = FALSE
);
devtools::install_github("rhondabacher/SCnorm")
devtools::install_github("catavallejos/BASiCS", ref = "batches")


devtools::install_github("hms-dbmi/pagoda2")
devtools::install_github("hms-dbmi/conos", ref="master")
