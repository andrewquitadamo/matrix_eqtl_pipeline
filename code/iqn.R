args = commandArgs(trailingOnly=TRUE)

if (length(args)==0)
{
  stop("Input file must be supplied.", call.=FALSE)
}

input_file = args[1]

inverse_quantile_norm <- function(filename)
{
	library(MatrixEQTL)

	gene = SlicedData$new()$LoadFile(filename);

	for( sl in 1:length(gene) ) {
	  mat = gene[[sl]];
	  mat = t(apply(mat, 1, rank, ties.method = "average"));
	  mat = qnorm(mat / (ncol(gene)+1));
	  gene[[sl]] = mat;
	}
	rm(sl, mat);

	gene <- as.matrix(gene)
	gene <- cbind(rownames(gene), gene)
	colnames(gene)[1] = "ID"
	write.table(gene,paste0(filename,'.qnorm'),col.names=T,row.names=F,quote=F,sep="\t")
}

inverse_quantile_norm(input_file)
