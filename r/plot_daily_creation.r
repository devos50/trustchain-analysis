library(ggplot2)
library(lubridate)
library(reshape2)

dat <- read.csv("../creation_stats.csv")
dat <- melt(dat, id=c("day"))
dat$day <- as.Date(dat$day)

print(dat)

p <- ggplot(dat, aes(x=day, y=value, fill=variable)) +
     geom_bar(stat="identity") +
     theme_bw() +
     theme(legend.position = c(0.1, 0.8)) +
     scale_x_date(limits = as.Date(c("2018-10-01", "2020-04-06")), expand = c(0, 0)) +
     xlab("Date") +
     ylab("Transactions")

ggsave(filename="block_creation.pdf", plot=p, width=10, height=3)
