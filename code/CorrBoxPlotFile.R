#' @export
CorrBoxPlot <- function (mEQTL,threshold,expr,genot,visual=FALSE,pdf_file="",crlt=0,cis=TRUE)
{
	# Inputs:
	#   mEQTL     - Matrix EQTL object with the eQTLs already collected
	#   threshold - FDR cutoff, only those eQTLs with equal or lower threshold will be taken into account
	#   expr      - Expression filename
	#   genot     - Genotype filename 
	#   visual    - If TRUE the script will display a box plot figure for each eQTL above the threshold
	#   pdf_file  - Filename for plots
	#   crlt      - Correlation cutoff (default 0)
	#   cis       - If TRUE only cis eQTLs are considered, otherwise trans eQTLS (default TRUE)
	#
	# Output: A vector with Pearson correlation scores for each eQTL that surpasses the given threshold
	#
	# NOTES:
	# Obviously the original files from which mEQTL object was computed must match on transcript, variants
	# and samples IDs included in expr and genot 
	#
	# R. Armananzas and Andrew Quitadamo

	library(readr)

	expr <- getFileData(expr) #nocov start
	genot <- getFileData(genot)
	mEQTL <- getFileData(mEQTL)

	index <- getIndex(mEQTL, threshold)
	eqtls <- getEQTLS(mEQTL, index)

	phenotype <- getEQTLPhenotypes(eqtls, expr)
	genotype <- getEQTLGenotypes(eqtls, genot)

	corr <- mapply(getCorr, phenotype, genotype) #nocov end

	if (visual)
	{
		if (pdf_file!="")
		{
			pdf(pdf_file)
			#par(mfcol = c(2, 2))
			#par(mfcol = c(1, 2))
		}

		for (i in 1:nrow(eqtls))
		{
			genotypes <- min(genotype[[i]],na.rm=T):max(genotype[[i]],na.rm=T)
			#Prepare the matrix
			pheno <- as.numeric(phenotype[[i]])
			values <- list();
			for (j in 1:length(genotypes))
			{
				values[[j]] <- pheno[which(genotype[[i]]==genotypes[j])]
			}
			#Plot the boxplots
			if (abs(corr[i])>=crlt)
			{
				boxplot(values,boxwex=0.5,ylab=paste(as.character(eqtls$gene[i])," expression"), names=genotypes,
					xlab=paste(as.character(eqtls$SNP[i])," genotype","\nCorrelation: ",format(corr[i],2),
					"P-value: ",format(eqtls$`p-value`[i],2)," FDR: ",format(eqtls$FDR[i],2)),
		  			main=paste(as.character(eqtls$SNP[i])," - ",as.character(eqtls$gene[i])))
			}
		}
		if (pdf_file!="")
		{
			dev.off()
		}
	}
	corr_df <- data.frame(names(corr),as.vector(corr))
	row.names(corr_df) <- NULL
	return(corr_df)
}

#TODO: Fix result when nothing is returned
getIndex <- function(mEQTL, threshold)
{
	return(which(mEQTL$FDR<=threshold))
}

getEQTLS <- function(mEQTL, index)
{
		return(mEQTL[index,])
}

getCorr <- function(phenotype, genotype)
{
	return(cor(as.numeric(phenotype),as.numeric(genotype), use="pairwise.complete.obs"))
}

getEQTLPhenotypes <- function(eqtls, expr)
{
	getPhenotypes <- getData(expr)
	return(Map(getPhenotypes, eqtls$gene))
}

getEQTLGenotypes <- function(eqtls, genot)
{
	getGenotypes <- getData(genot)
	return(Map(getGenotypes, eqtls$SNP))
}

getData <- function(data)
{
	function(eqtlID)
	{
		return(data[which(data[,1]==as.character(eqtlID)),2:ncol(data)])
	}
}

getFileData <- function(filename)
{
	suppressMessages(return(read_delim(filename, delim='\t')))
}
