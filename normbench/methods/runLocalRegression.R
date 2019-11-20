# runner function
# sce - single cell experiment data structure
runLocalRegressionFromSCE <- function(sce,n.cores=detectCores()) {
  # extract count matrix
  counts <- sce@assays@data@counts;
  runLocalRegressionFromMatrix(counts,n.cores=n.cores)
}

# cd - matrix, should be castable to dgCMatrix; rows - genes; columns- cells
runLocalRegressionFromMatrix <- function(cd,n.cores=detectCores()) {
  cd <- as(cd,'dgCMatrix'); # assert format
  # get the count matrix
  #cd <- seurat.object@assays$RNA@counts;
  rownames(cd) <- make.unique(rownames(cd))

  # run local regression with an increasing size of clusters
  r <- strawnorm(cd,res=c(0.5,1,2,3),n.cores=n.cores);
  # return normalized matrix
  x <- r$counts;
  # normalize gene variance
  x@x <- x@x*rep(r$misc[['varinfo']][colnames(x),'gsf'],diff(x@p))
  x
}

#### 
# the method itself
require(conos)
require(edgeR)
require(pagoda2)
require(parallel)
require(Matrix)
require(robustbase)


# strawman normalization
# local regression - iterative regression of each cell against combined expression profiles of local clusters
strawnorm <- function(cd,res=c(0.5,1,2,3),fix.init.depth=NULL,n.cores=30,nPcs=30,n.odgenes=2e3,k=30,use.edgeR.correction=TRUE,verbose=TRUE) {

  # refine lib sizes using robust regression against the cluster total
  refine.lib.sizes <- function(counts,groups) {

    # collapse all molecules within clusters into a meta-cell
    lvec <- conos:::colSumByFactor(counts,as.factor(groups))[-1,,drop=F];
    lvec <- t(lvec/pmax(1,Matrix::rowSums(lvec)))*1e4

    x <- pagoda2:::papply(1:length(levels(groups)),function(j) {
      ii <- names(groups)[which(groups==j)]
      if(length(ii)<2) { return(setNames(c(rowSums(counts[ii,])/1e4),ii)) } # if it's just one cell, don't bother
      av <- lvec[,j]
      avi <- which(av>0)
      av <- av[avi]
      cvm <- as.matrix(counts[ii,avi])
      
      x <- unlist(lapply(ii,function(i) {
        cv <- cvm[i,]
        as.numeric(coef(robustbase::glmrob(cv~av+0,family=poisson(link='identity'),start=sum(cv)/1e4)))
      }))
      names(x) <- ii;
      x
    },n.cores=n.cores)

    
    if(use.edgeR.correction) {
      # even out cluster scales against each other
      f <- edgeR::calcNormFactors(lvec)
      f <- f/exp(mean(log(f)))
      x <- lapply(1:length(x),function(i) {
        x[[i]]*f[i]
      })
    }

    lib.sizes <- unlist(x)[rownames(counts)]
    # global scaling
    lib.sizes <- lib.sizes/mean(lib.sizes)*mean(Matrix::rowSums(counts))
  }

  # subsample columns of a sparse matrix to approximately a desired depth
  subsample.cell.depth <- function(m,depth) {
    p.sample <- pmin(1,rep(depth/colSums(m),diff(m@p)))
    m@x <- as.numeric(rbinom(length(m@x),m@x,p.sample))
    m
  }



  internal.norm.loop <- function(cd,groups=NULL,res=1) {
    if(!is.null(groups)) {
      lib.sizes <- refine.lib.sizes(t(cd),groups); # regression-based estimates
    } else {
      lib.sizes <- NULL; # use number of molecules estimate
    }
    # make a p2 object
    p2process(cd,lib.sizes=lib.sizes,n.cores=n.cores,nPcs=nPcs,k=k,n.odgenes=n.odgenes,res=res,verbose=F)
  }

  ccd <- cd;
  if(!is.null(fix.init.depth)) {
    if(is.logical(fix.init.depth) & fix.init.depth) {
      init.depth <- min(colSums(cd))
      cat("limiting cell depth for the initial round to the smallest cell: ",init.depth,"\n")
    } else if(is.numeric(fix.init.depth)) {
      init.depth <- fix.init.depth;
      cat("limiting cell depth for the initial round to the specified: ",init.depth,"\n")
    }
    # subsample cells
    ccd <- subsample.cell.depth(ccd,init.depth)
  }

  
  res <- c(res,res[length(res)])

  cat("initial processing ...")
  r <- internal.norm.loop(ccd,res=res[1],groups=NULL)
  cat(" done\n")

  cat("processing iterations ");
  for(i in res) {
    groups <- r$clusters$PCA[[1]];
    r <- internal.norm.loop(cd,res=i,groups=groups)
    cat(".")
  }
  cat(" done\n")
  return(r);
}


# basic p2 processing
p2process <- function(cd,lib.sizes=NULL,n.cores=30,nPcs=30,n.odgenes=2e3,res=1,k=30,verbose=FALSE) {
  r <- Pagoda2$new(cd,lib.sizes=lib.sizes,log.scale=TRUE, n.cores=n.cores,verbose=verbose)
  # varnorm, PCA, kNN, cluster
  r$adjustVariance(plot=F,gam.k=10,verbose=F);
  r$calculatePcaReduction(nPcs=nPcs,n.odgenes=n.odgenes,verbose=F);
  r$makeKnnGraph(k=k,type='PCA',center=T,distance='cosine',verbose=F);
  r$getKnnClusters(type='PCA',method=conos:::leiden.community,resolution=res)
  r
}

