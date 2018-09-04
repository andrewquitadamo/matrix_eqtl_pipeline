library(peer)

get_colname <- function(number) {
  return(paste0("PEER", number))
}

peer_function <- function(input_file, numfactors) {
  expr <- read.table(input_file, header = T, row.names = 1, check.names = F)

  model <- PEER();
  PEER_setPhenoMean(model, t(as.matrix(expr)));
  PEER_setNk(model, numfactors);
  PEER_update(model);

  factors <- PEER_getX(model);
  factors <- t(factors);
  colnames(factors) <- colnames(expr);


  rownames(factors) <- sapply(seq_along(1:nrow(factors)), get_colname);
  factors <- cbind(rownames(factors), factors);
  colnames(factors)[1] <- "ID";
  return(data.frame(factors))
}
