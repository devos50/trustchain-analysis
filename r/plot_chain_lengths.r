library(ggplot2)

dat <- read.csv("../chain_lengths.csv")

dat <- dat[dat$blocks < 1000,]

p <- ggplot(dat, aes(blocks)) +
     stat_ecdf(geom="step") +
     theme_bw() +
     xlab("Transactions in individual ledger") +
     ylab("ECDF")

ggsave(filename="chain_lengths.pdf", plot=p, width=5, height=3)
