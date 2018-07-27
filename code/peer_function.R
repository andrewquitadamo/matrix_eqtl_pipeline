library(peer)
#args = commandArgs(trailingOnly=TRUE)

#if (length(args)!=3)
#{
#  stop("Input file, id and number of factors must be supplied.", call.=FALSE)
#}

#input_file = args[1]
#id = args[2]
#numfactors = args[3]

get_colname <- function(number)
{
	return(paste0('PEER',number))
}

peer_function <- function(input_file,numfactors)
{
	expr <- read.table(input_file, header=T, row.names=1, check.names=F)

	model = PEER()
	PEER_setPhenoMean(model,t(as.matrix(expr)))
	PEER_setNk(model,numfactors)
	PEER_update(model)

	factors = PEER_getX(model)
	factors <- t(factors)
	colnames(factors) <- colnames(expr)


	rownames(factors) <- sapply(seq_along(1:nrow(factors)),get_colname)
	factors<-cbind(rownames(factors),factors)
	colnames(factors)[1]<-"ID"
	return(data.frame(factors))
}

#factors <- peer_function(input_file, numfactors)
#write.table(factors, paste0('data/',id,'_peer_factors_',numfactors), col.names=T,row.names=F,sep="\t",quote=F)
