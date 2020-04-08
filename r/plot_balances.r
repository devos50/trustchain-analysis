library(ggplot2)

options(scipen=10000)

dat <- read.csv("../balances.csv")
dat$balance <- dat$total_up - dat$total_down
dat$balance <- dat$balance / 1024 / 1024 / 1024

p <- ggplot(dat, aes(balance)) +
     stat_ecdf(geom="step") +
     theme_bw() +
     xlab("Bandwidth balance (GB)") +
     ylab("ECDF")

ggsave(filename="balances.pdf", plot=p, width=10, height=3)

# Negative balances ECDF
dat_filtered <- dat[dat$balance <= 0,]
dat_filtered <- dat_filtered[dat_filtered$balance >= -100,]

p <- ggplot(dat_filtered, aes(balance)) +
     stat_ecdf(geom="step") +
     theme_bw() +
     xlab("Bandwidth balance (GB)") +
     ylab("ECDF")

ggsave(filename="balances_negative.pdf", plot=p, width=5, height=3)

# Postitive balances ECDF
dat_filtered <- dat[dat$balance >= 0,]
dat_filtered <- dat_filtered[dat_filtered$balance <= 5,]

p <- ggplot(dat_filtered, aes(balance)) +
     stat_ecdf(geom="step") +
     theme_bw() +
     xlab("Bandwidth balance (GB)") +
     ylab("ECDF")

ggsave(filename="balances_positive.pdf", plot=p, width=5, height=3)
