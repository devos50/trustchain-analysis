library(ggplot2)

options(scipen=10000)

dat <- read.csv("../balances.csv")
dat$balance <- dat$total_up - dat$total_down
dat$total_up <- dat$total_up / 1024 / 1024 / 1024
dat$total_down <- dat$total_down / 1024 / 1024 / 1024
dat$freeride <- ifelse((dat$total_up - dat$total_down) < -5, "freerider", "no freerider")
dat$balance <- dat$balance / 1024 / 1024 / 1024

# Scatter plot
p <- ggplot(dat, aes(x=total_down, y=total_up, col=dat$freeride)) +
            geom_point(size=0.5) +
            scale_color_manual(values=c('red', 'green')) +
            scale_x_log10(breaks=c(0.01, 1, 100, 10000)) +
            scale_y_log10() +
            xlab("Total download (GB)") +
            ylab("Total upload (GB)") +
            theme_bw() +
            theme(legend.position = c(0.25, 0.83), legend.box.margin=margin(c(20,20,20,20)), legend.background = element_rect(color = "#333333", size = 0.7, linetype = "solid"), legend.text=element_text(size=12), legend.title=element_text(size=12, face="bold")) +
            guides(color=guide_legend(title="Users"))
ggsave(filename="balances_scatter.pdf", plot=p, width=4, height=3.5)

# p <- ggplot(dat, aes(balance)) +
#      stat_ecdf(geom="step") +
#      theme_bw() +
#      xlab("Bandwidth balance (GB)") +
#      ylab("ECDF")
#
# ggsave(filename="balances.pdf", plot=p, width=10, height=3)
#
# # Negative balances ECDF
# dat_filtered <- dat[dat$balance <= 0,]
# dat_filtered <- dat_filtered[dat_filtered$balance >= -100,]
#
# p <- ggplot(dat_filtered, aes(balance)) +
#      stat_ecdf(geom="step") +
#      theme_bw() +
#      xlab("Bandwidth balance (GB)") +
#      ylab("ECDF")
#
# ggsave(filename="balances_negative.pdf", plot=p, width=5, height=3)
#
# # Postitive balances ECDF
# dat_filtered <- dat[dat$balance >= 0,]
# dat_filtered <- dat_filtered[dat_filtered$balance <= 5,]
#
# p <- ggplot(dat_filtered, aes(balance)) +
#      stat_ecdf(geom="step") +
#      theme_bw() +
#      xlab("Bandwidth balance (GB)") +
#      ylab("ECDF")
#
# ggsave(filename="balances_positive.pdf", plot=p, width=5, height=3)
