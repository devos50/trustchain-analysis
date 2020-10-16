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
     theme(legend.position = c(0.11, 0.8), axis.text.x = element_text(angle = 90), legend.box.background = element_rect(colour = "black"), legend.title=element_blank()) +
     scale_x_date(date_breaks="1 month", date_labels="%y-%m-%d", expand = c(0, 0)) +
     scale_fill_discrete(name="") +
     xlab("Date") +
     ylab("Proposals") +
     geom_vline(xintercept=as.numeric(as.Date("2020-06-18")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2020-07-01"), label="v7.5.0", y=200000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2020-02-01")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2020-02-12"), label="v7.4.0", y=200000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2019-08-27")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2019-09-08"), label="v7.3.0", y=200000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2019-01-31")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2019-02-11"), label="v7.2.0", y=200000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2018-10-09")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2018-10-21"), label="v7.1.0", y=200000, hjust=1, angle=90)

ggsave(filename="block_creation.pdf", plot=p, width=10, height=3)
