install.packages("Seurat")
install.packages("devtools")

library(devtools)
devtools::install_github("rhondabacher/SCnorm")

install.packages(c("RcppEigen", "urltools", "Rtsne","BiocManager","robustbase"))

devtools::install_github("hms-dbmi/pagoda2")
BiocManager::install(c("GO.db", "org.Hs.eg.db","org.Mm.eg.db", "pcaMethods","DESeq2","edgeR","BiocGenerics"), suppressUpdates=TRUE);
devtools::install_github("hms-dbmi/conos", ref="master")
