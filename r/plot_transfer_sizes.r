library(ggplot2)

options(scipen=10000)

dat <- read.csv("../transfer_sizes.csv")

# Remove values > 50MB
dat <- dat[dat$value < 50,]

p <- ggplot(dat, aes(x=value, y=frequency)) +
     geom_bar(stat="identity") +
     theme_bw() +
     xlab("Transaction size (MB downloaded)") +
     ylab("Frequency")

ggsave(filename="transfer_sizes_to_50.pdf", plot=p, width=5, height=3)


# Plot tranfer size under 5MB
dat <- read.csv("../transfer_sizes_under_5mb.csv")

# Remove values < 1000KB
dat <- dat[dat$value >= 1000,]

p <- ggplot(dat, aes(x=value, y=frequency)) +
     geom_bar(stat="identity") +
     theme_bw() +
     xlab("Transaction size (MB downloaded)") +
     ylab("Frequency")

ggsave(filename="transfer_sizes_under_5mb.pdf", plot=p, width=5, height=3)