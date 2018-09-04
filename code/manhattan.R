suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
suppressMessages(library(readr))


get_snp_positions  <-  function(gene_table, snp_position_table) {
  snp_table <- inner_join(gene_table, snp_position_table, by = c("SNP" = "snpid"))
  return(snp_table)
}


get_max_chromosome_position <- function(combined_positions) {
  max_chromosome_position <- vector()
  for (i in 1:22) {
    max_chromosome_position[i] <- max(combined_positions[which(combined_positions$chr == i), ]$pos)
  }
  return(max_chromosome_position)
}

get_cumulative_max_positions <- function(max_chromosome_positions) {
  cumulative_max_positions <- vector()
  for (i in 1:22) {
    cumulative_max_positions[i] <- sum(as.numeric(max_chromosome_positions[1:i - 0]))
  }
  cumulative_max_positions <- c(0, cumulative_max_positions)
  return(cumulative_max_positions)
}

get_midpoints <- function(cumulative_max_positions) {
  midpoints <- vector()
  for (i in 1:22) {
    midpoints[i] <- (cumulative_max_positions[i] + cumulative_max_positions[i + 1]) / 2
  }
  return(midpoints)
}

get_breaks <- function(cumulative_max_positions, midpoints) {
  breaks <- vector()
  for (i in 1:22) {
    breaks <- c(breaks, cumulative_max_positions[i], midpoints[i])
  }
  breaks <- c(breaks, cumulative_max_positions[23])
  return(breaks)
}


get_chr_dat <- function(eqtl_positions, cumulative_max_positions) {
  chr_dat_full <- data.frame()
  for (chr in 1:22) {
    chr_dat <- eqtl_positions[which(eqtl_positions$chr == chr), ]
    chr_dat$pos <- chr_dat$pos + cumulative_max_positions[chr]
  chr_dat_full <- rbind(chr_dat_full, chr_dat)
  }
  chr_dat_full$FDR <-  -log10(chr_dat_full$FDR)
  return(chr_dat_full)
}

manhattan <- function(cis_results, positions, pdf_file) {
combined_gene_cis_results <- suppressMessages(read_delim(cis_results, "\t", escape_double = FALSE, trim_ws = TRUE))
combined_positions <- suppressMessages(read_delim(positions, "\t", escape_double = FALSE, trim_ws = TRUE))
eqtl_positions <- get_snp_positions(combined_gene_cis_results, combined_positions)
max_chromosome_position <- get_max_chromosome_position(combined_positions)
cumulative_max_positions <- get_cumulative_max_positions(max_chromosome_position)
midpoints <- get_midpoints(cumulative_max_positions)
breaks <- get_breaks(cumulative_max_positions, midpoints)
chrom <- c("", "1", "", "2", "", "3", "", "4", "", "5", "", "6", "", "7", "", "8", "", "9", "", "10", "", "11", "", "12", "", "13", "", "14", "", "15", "", "16", "", "17", "", "18", "", "19", "", "20", "", "21", "", "22", "")
chr_dat_full <- get_chr_dat(eqtl_positions, cumulative_max_positions)

pdf(pdf_file)
print(ggplot() + geom_point(data = chr_dat_full, aes(pos, FDR, color = factor(chr))) +
        labs(y = "-log10(FDR)") + ggtitle("Manhattan Plot") +
        theme(plot.title = element_text(hjust = 0.5), axis.text = element_text(size = 5), legend.position = "none") +
        scale_x_continuous(name = "Chromosome", breaks = breaks, labels = chrom) +
    scale_color_manual(values = rep(c("#7FC97F", "#BEAED4", "#FDC086", "#FFFF99", "#386CB0", "#F0027F", "#BF5B17", "666666"), 3)))
dev.off()

}
