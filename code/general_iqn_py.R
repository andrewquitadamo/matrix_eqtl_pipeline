inverse_quantile_norm <- function(filename)
{
	{sink("/dev/null"); gene = SlicedData$new()$LoadFile(filename);sink();}

	for(sl in 1:length(gene)) {
	  mat = gene[[sl]];
	  mat = t(apply(mat, 1, rank, ties.method = "average"));
	  mat = qnorm(mat / (ncol(gene)+1));
	  gene[[sl]] = mat;
	}
	rm(sl, mat);

	gene <- as.matrix(gene)
	gene <- cbind(rownames(gene), gene)
	colnames(gene)[1] = "ID"

	return(gene)
}
