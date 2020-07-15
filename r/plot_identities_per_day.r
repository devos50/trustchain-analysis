library(ggplot2)

dat <- read.csv("../new_identities_per_day.csv")

dat <- dat[order(as.Date(dat$day, format = "%Y-%m-%d")),]
dat$day <- as.Date(dat$day)

dat$cumsum <- cumsum(dat$new_identities)

p <- ggplot(dat, aes(x=day, y=cumsum)) +
     geom_line() +
     scale_x_date(date_breaks="1 month") +
     theme_bw() +
     xlab("Date") +
     ylab("Total identities") +
     theme(axis.text.x = element_text(angle = 90))

ggsave(filename="identities_per_day.pdf", plot=p, width=10, height=3)
