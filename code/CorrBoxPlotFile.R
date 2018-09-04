#' @export
corr_boxplot <- function (meqtl, threshold, expr, genot, visual = FALSE, pdf_file = "", crlt = 0, cis = TRUE) {
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

  expr <- get_file_data(expr) #nocov start
  genot <- get_file_data(genot)
  meqtl <- get_file_data(meqtl)

  index <- get_index(meqtl, threshold)
  eqtls <- get_eqtls(meqtl, index)

  phenotype <- get_eqtl_phenotypes(eqtls, expr)
  genotype <- get_eqtl_genotypes(eqtls, genot)

  corr <- mapply(get_corr, phenotype, genotype) #nocov end

  if (visual) {
    if (pdf_file != "") {
      pdf(pdf_file)
    }

    for (i in 1:nrow(eqtls)) {
      genotypes <- min(genotype[[i]], na.rm = T):max(genotype[[i]], na.rm = T)
      #Prepare the matrix
      pheno <- as.numeric(phenotype[[i]])
      values <- list();
      for (j in 1:length(genotypes)) {
        values[[j]] <- pheno[which(genotype[[i]] == genotypes[j])]
      }
      #Plot the boxplots
      if (abs(corr[i]) >= crlt) {
        boxplot(values, boxwex = 0.5, ylab = paste(as.character(eqtls$gene[i]), " expression"), names = genotypes,
          xlab = paste(as.character(eqtls$SNP[i]), " genotype", "\nCorrelation: ", format(corr[i], 2),
          "P-value: ", format(eqtls$`p-value`[i], 2), " FDR: ", format(eqtls$FDR[i], 2)),
            main = paste(as.character(eqtls$SNP[i]), " - ", as.character(eqtls$gene[i])))
      }
    }
    if (pdf_file != "") {
      dev.off()
    }
  }
  corr_df <- data.frame(names(corr), as.vector(corr))
  row.names(corr_df) <- NULL
  return(corr_df)
}

#TODO: Fix result when nothing is returned
get_index <- function(meqtl, threshold) {
  return(which(meqtl$FDR <= threshold))
}

get_eqtls <- function(meqtl, index) {
    return(meqtl[index, ])
}

get_corr <- function(phenotype, genotype) {
  return(cor(as.numeric(phenotype), as.numeric(genotype), use = "pairwise.complete.obs"))
}

get_eqtl_phenotypes <- function(eqtls, expr) {
  get_phenotypes <- get_data(expr)
  return(Map(get_phenotypes, eqtls$gene))
}

get_eqtl_genotypes <- function(eqtls, genot) {
  get_genotypes <- get_data(genot)
  return(Map(get_genotypes, eqtls$SNP))
}

get_data <- function(data) {
  function(eqtl_id) {
    return(data[which(data[, 1] == as.character(eqtl_id)), 2:ncol(data)])
  }
}

get_file_data <- function(filename) {
  suppressMessages(return(read_delim(filename, delim = "\t", progress = F)))
}
