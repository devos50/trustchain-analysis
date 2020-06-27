library(ggplot2)

dat <- read.csv("../combined_tc_reject_balances.csv")
dat$balance <- dat$balance / 1024 / 1024 / 1024

# Filter out balance lower or higher than 100GB
dat_filtered <- dat[dat$balance >= -500,]
dat_filtered <- dat_filtered[dat_filtered$balance < 50,]

p <- ggplot(dat_filtered, aes(x=balance, group=type, colour=type)) +
     stat_ecdf(aes(linetype=type), geom="step") +
     theme_bw() +
     theme(legend.position=c(0.2, 0.7), legend.box.background = element_rect(colour = "black"), legend.margin=margin(c(3, 3, 3, 3)), legend.spacing.y = unit(0.0, 'cm')) +
     scale_linetype_manual(labels=c("Reject event", "All"), values=c("solid", "longdash")) +
     scale_color_manual(labels=c("Reject event", "All"), values=c("red", "#25b010")) +
     labs(color='Balance', linetype='Balance') +
     xlab("Bandwidth balance (GB)") +
     ylab("ECDF")

ggsave(filename="exit_node_rejects.pdf", plot=p, width=4, height=2)
