library(plyr)
library(RJSONIO)

data2 = fromJSON("anovainput.json")#import the data
l <- list(data2)#convert to a list of lists
df <- ldply(l, data.frame)#convert to a df

library(tidyverse)
library(ggpubr)
library(rstatix)
library(dplyr)

sumstats = df %>%
	group_by(colour, motion, render) %>%
	get_summary_stats(object, type = "mean_sd")

bxp <- ggboxplot(
  df, x = "render", y = "object",
  color = "motion", palette = "jco",
  facet.by = "colour", short.panel.labs = FALSE
  )
bxp

outliers = df %>%
  group_by(colour, motion, render) %>%
  identify_outliers(object)

dfx = anti_join(df, outliers)

bxp2 <- ggboxplot(
  dfx, x = "render", y = "object",
  color = "motion", palette = "jco",
  facet.by = "colour", short.panel.labs = FALSE
  )
bxp2

res.aov <- anova_test(
  data = dfx, dv = object, wid = PID,
  between = render, within = c(colour, motion)
  )
get_anova_table(res.aov)

two.way <- dfx %>%
  group_by(render) %>%
  anova_test(dv = object, wid = PID, within = c(colour, motion))
two.way

#get_anova_table(two.way)

two.way2 <- dfx %>%
  group_by(colour) %>%
  anova_test(dv = object, wid = PID, within = c(motion), between = c(render))
two.way2

two.way3 <- dfx %>%
  group_by(motion) %>%
  anova_test(dv = object, wid = PID, within = c(colour), between = c(render))
two.way3


colour.effect <- dfx %>%
  group_by(render, motion) %>%
  anova_test(dv = object, wid = PID, within = colour) %>%
  get_anova_table()

colour.effect

motion.effect <- dfx %>%
  group_by(render, colour) %>%
  anova_test(dv = object, wid = PID, within = motion) %>%
  get_anova_table()

motion.effect

render.effect <- dfx %>%
  group_by(motion, colour) %>%
  anova_test(dv = object, wid = PID, between = render) %>%
  get_anova_table()

render.effect

#todo create pairwise comps for all conditions
# compute pairwise comparisons
pwc <- df %>%
  group_by(render, colour) %>%
  pairwise_t_test(
    object ~ motion, paired = TRUE, 
    p.adjust.method = "bonferroni"
    ) %>%
  select(-statistic, -df) # Remove details
pwc

pwc2<- df %>%
  group_by(render, motion) %>%
  pairwise_t_test(
    object ~ colour, paired = TRUE, 
    p.adjust.method = "bonferroni"
    ) %>%
  select(-statistic, -df) # Remove details
pwc2

extras = subset(df, subset = (render == 'VX2' & PID > 159))
dfex = anti_join(df, extras)

pwc3<- dfex %>%
  group_by(colour, motion) %>%
  pairwise_t_test(
    object ~ render, paired = TRUE, 
    p.adjust.method = "bonferroni"
    )
as.data.frame(pwc3)