library(ggplot2)

dat <- read.csv("../new_identities_per_day.csv")

dat <- dat[order(as.Date(dat$day, format = "%Y-%m-%d")),]
dat$day <- as.Date(dat$day)

dat$cumsum <- cumsum(dat$new_identities)

p <- ggplot(dat, aes(x=day, y=cumsum)) +
     geom_line() +
     scale_x_date(date_breaks="1 month", date_labels="%y-%m-%d") +
     theme_bw() +
     xlab("Date (Year-Month-Day)") +
     ylab("Unique Identities") +
     theme(axis.text.x = element_text(angle = 90, size=8)) +
     geom_vline(xintercept=as.numeric(as.Date("2020-06-18")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2020-07-04"), label="v7.5.0", y=35000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2020-02-01")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2020-02-15"), label="v7.4.0", y=35000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2019-08-27")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2019-09-11"), label="v7.3.0", y=80000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2019-01-31")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2019-02-14"), label="v7.2.0", y=80000, hjust=1, angle=90) +
     geom_vline(xintercept=as.numeric(as.Date("2018-10-09")), size=0.5, alpha=0.6) +
     annotate("text", x=as.Date("2018-10-24"), label="v7.1.0", y=80000, hjust=1, angle=90)

ggsave(filename="identities_per_day.pdf", plot=p, width=4, height=2)
