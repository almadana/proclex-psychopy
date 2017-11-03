############################################################################
#
# BACS - Similarity matrice analyses
# Article Vidal, Content, & Chetail
#
# Created February 2016
# Updated October 2016
#
# (C) F. Chetail
#
############################################################################

library(dplyr)
library(tidyr)
library(ggplot2)
library(grid)
library(gridExtra)
library(cowplot)
library(extrafont) # to see fonts
library(ape) # transform dendrograms

rm(list=ls())
#root1="~/Desktop/rawData" # should be updated according to personnal paths
#root2="~/Desktop/appendixC"
root1="~/Documents/WORK/RCH/Articles/Soumis/VCC_tool/ARTICLE_OK/Revision-1/Figures/rawData"
root2="~/Documents/WORK/RCH/Articles/Soumis/VCC_tool/ARTICLE_OK/Revision-1/Figures/appendixC"

#font_import() # to import font (should be done each time new fonts are installed: can be very long!!)
#loadfonts() # to see listing of font (way to get accurate names)

#####################################################################################
############################ BASIC STATS & DISTRIBUTIONS ############################
#####################################################################################
setwd(root1)

########## UPLOAD RAW FILES & CLEANING
b1 = read.delim("BACS_1_lowerUppercaseSans.txt", header=T)
b1$temp = tolower(b1$Ref) 
b1$case[b1$Ref==b1$temp]="lower"
b1$case[b1$Ref!=b1$temp]="upper"

b1 = select(b1, Ref, Cible, Paire, rating.response_raw, rating.rt_raw, numPs, case)
colnames(b1) = c("one", "two", "pair", "sim", "rt", "numPs", "case")
b1l = b1 %>% filter(case=="lower") %>% select(-case) %>% data.frame()
b1u = b1 %>% filter(case=="upper") %>% select(-case) %>% data.frame()

b2l = read.delim("BACS_2_lowercaseSans.txt", header=T)
b2u = read.delim("BACS_2_uppercaseSans.txt", header=T)
b2ls = read.delim("BACS_2_lowercaseSerif.txt", header=T)
b2us = read.delim("BACS_2_uppercaseSerif.txt", header=T)

b2l = select(b2l, Lettre1, Lettre2, Paires, rating.response_raw, rating.rt_raw, numPs)
b2u = select(b2u, Lettre1, Lettre2, Paires, rating.response_raw, rating.rt_raw, numPs)
b2ls = select(b2ls, Lettre1, Lettre2, Paires, rating.response_raw, rating.rt_raw, numPs)
b2us = select(b2us, Lettre1, Lettre2, Paires, rating.response_raw, rating.rt_raw, numPs)

colnames(b2l) = c("one", "two", "pair", "sim", "rt", "numPs")
colnames(b2u) = c("one", "two", "pair", "sim", "rt", "numPs")
colnames(b2ls) = c("one", "two", "pair", "sim", "rt", "numPs")
colnames(b2us) = c("one", "two", "pair", "sim", "rt", "numPs")

# b1l = BACS 1 lowercase
# b1u = BACS 1 uppercase
# b2l = BACS 2 lowercase sans
# b2u = BACS 2 uppercase sans
# b2ls = BACS 2 lowercase serif
# b2us = BACS 2 uppercase serif

# Some raw data have been modified to remove name of participants
# Check for anonymity
unique(b1l$numPs)
unique(b1u$numPs)
unique(b2l$numPs)
unique(b2u$numPs)
unique(b2ls$numPs)
unique(b2us$numPs)

### altogether
b1l$set = "b1l"
b1u$set = "b1u"
b2l$set = "b2l"
b2u$set = "b2u"
b2ls$set = "b2ls"
b2us$set = "b2us"
d = rbind(b1l, b1u, b2l, b2u, b2ls, b2us)

########## REMOVING BAD PARTICIPANTS
# BACS-2 lowercase sans: 
# - Ps H didn't get the instructions (used only 1/0)
# - Ps D stopped at block 9
# BACS-2 uppercase sans: 
# - Ps LV mixed the instructions (used 0 for similar pairs),
# - Ps MTS used only the extreme points of the scale (and rated 1 many very dissimilar pairs)

d$id = paste0(d$set,d$numPs)
d = filter(d, id!="b2lH" & id!="b2lD")
d = filter(d, id!="b2uLV" & id!="b2uMTS")
d = select(d, -id)


################### SIMILARITY ACCORDING TWO ORDERS & DISTRIBUTIONS
# identifying same pairs
d$id = 0
d$id[d$one==d$two] = 1

##### B1L
# Basic stats
d %>% filter(set=="b1l") %>% summarize(mean(sim))
d %>% filter(set=="b1l" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b1l" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b1l" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

# Scatterplot
B1L_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-1 lowercase")

# distribution
B1L_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-1 lowercase")+
  scale_y_continuous(limits = c(0, 220))


##### B1U
# Basic stats
d %>% filter(set=="b1u") %>% summarize(mean(sim))
d %>% filter(set=="b1u" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b1u" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b1u" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

# scatterplot
B1U_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-1 uppercase")

# distribution
B1U_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-1 uppercase")+
  scale_y_continuous(limits = c(0, 220))


##### B2L
# Basic stats
d %>% filter(set=="b2l") %>% summarize(mean(sim))
d %>% filter(set=="b2l" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b2l" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b2l" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

# scatterplot
B2L_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-2 Sans lowercase")

# distribution
B2L_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-2 Sans lowercase")+
  scale_y_continuous(limits = c(0, 220))

##### B2U
# Basic stats
d %>% filter(set=="b2u") %>% summarize(mean(sim))
d %>% filter(set=="b2u" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b2u" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b2u" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="1") %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

B2U_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-2 Sans uppercase")

# distribution
B2U_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-2 Sans uppercase")+
  scale_y_continuous(limits = c(0, 220))

##### BMLS
# Basic stats
d %>% filter(set=="b2ls") %>% summarize(mean(sim))
d %>% filter(set=="b2ls" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b2ls" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b2ls" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

# scatterplot
B2LS_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-2 Serif lowercase")

# distribution
B2LS_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-2 Serif lowercase")+
  scale_y_continuous(limits = c(0, 220))

##### B2US
# Basic stats
d %>% filter(set=="b2us") %>% summarize(mean(sim))
d %>% filter(set=="b2us" & id==1) %>% summarize(mean(sim))
d %>% filter(set=="b2us" & id!=1) %>% select(sim) %>% max()

temp = filter(d, set=="b2us" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="VV") %>% data.frame()
temp = temp %>% group_by(pair) %>% mutate(idPair = paste(sort(c(as.character(one), as.character(two))),collapse="")) %>% data.frame()
temp$ordre=0
temp$ordre[substr(temp$idPair,1,1)==temp$one] = 1 # create order index
temp = temp %>% group_by(ordre) %>% arrange(idPair) %>% mutate(num = 1:length(idPair)) %>% data.frame()

A = temp %>% filter(ordre==0) %>% select(sim)
B = temp %>% filter(ordre==1) %>% select(sim)
cor(A,B) # correlations between to the 2 orders

# scatterplot
B2US_corr = ggplot(data.frame(A,B), aes(x=sim, y=sim.1)) + geom_point() +
  labs(x = "Estimated similarity - Order 1") +
  labs(y = "Estimated similarity - Order 2") +
  labs(title = "BACS-2 Serif uppercase")

# distribution
B2US_distr = ggplot(temp, aes(sim)) + geom_histogram(binwidth=.05, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "BACS-2 Serif uppercase")+
  scale_y_continuous(limits = c(0, 220))


########## DISTRIBUTIONS IN THE LATIN ALPHABET
setwd("~/Documents/WORK/RCH/Articles/Soumis/VCC_tool/ARTICLE_OK/Revision-1/Figures")
sl = read.delim("Simpson_MIN.txt", header=T)
su = read.delim("Simpson_MAJ.txt", header=T)  
sl = gather(sl, key = L2, value = sim, -1)
su = gather(su, key = L2, value = sim, -1)
sl = filter(sl, !is.na(sim))
su = filter(su, !is.na(sim))

SL = ggplot(sl, aes(sim)) + geom_histogram(binwidth=.25, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "Latin alphabet lowercase") +
  scale_y_continuous(limits = c(0, 220))

SU = ggplot(su, aes(sim)) + geom_histogram(binwidth=.25, color="black", fill="white") + 
  labs(x = "Estimated similarity") +
  labs(y = "Counts") +
  labs(title = "Latin alphabet uppercase") +
  scale_y_continuous(limits = c(0, 220)) 

################ FIGURES ################
plot_grid(B1L_corr, B1U_corr, B2L_corr, B2U_corr, B2LS_corr, B2US_corr, labels=c("A", "B", "C", "D", "E","F"), ncol = 2, nrow = 3) # Figure 11 - pdf A4
plot_grid(SL, SU, B1L_distr, B1U_distr, B2L_distr, B2U_distr, B2LS_distr, B2US_distr, labels=c("A", "B", "C", "D","E","F","G","H"), ncol = 2, nrow = 4) # Figure 12 - pdf A4


####################################################################
############################ HEAT MAPS #############################
####################################################################
# font_import() 
fonts()

# BACS
temp = filter(d, set=="b1l" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
B1L_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS1", size=20)) +
  theme(axis.text.y = element_text(family="BACS1", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(legend.position="none") +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-1 lowercase")

temp = filter(d, set=="b1u" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
B1U_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS1", size=20)) +
  theme(axis.text.y = element_text(family="BACS1", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-1 uppercase")

temp = filter(d, set=="b2l" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
B2L_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS2sans", size=20)) +
  theme(axis.text.y = element_text(family="BACS2sans", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(legend.position="none") +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-2 Sans lowercase")

temp = filter(d, set=="b2u" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
B2U_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS2sans", size=20)) +
  theme(axis.text.y = element_text(family="BACS2sans", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-2 Sans uppercase")

temp = filter(d, set=="b2ls" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
B2LS_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS2serif", size=20)) +
  theme(axis.text.y = element_text(family="BACS2serif", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  theme(legend.position="none") +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-2 Serif lowercase")

temp = filter(d, set=="b2us" & id!=1) %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==8) %>% data.frame()
B2US_heat = ggplot(temp, aes(one, two, fill = sim)) + geom_raster() +
  scale_fill_gradient(low = "white", high = "black", limits=c(0,1)) +
  theme(axis.text.x = element_text(family="BACS2serif", size=20)) +
  theme(axis.text.y = element_text(family="BACS2serif", size=20)) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_blank()) +
  labs(fill = "Estimated\nSimilarity") +
  labs(title = "BACS-2 Serif uppercase")

grid.arrange(B1L_heat, B1U_heat, B2L_heat, B2U_heat, B2LS_heat, B2US_heat, widths=c(45/50, 55/50), ncol=2, nrow=3) # jpg, 1200x600
# Figure 13, 918x1298

####################################################################
############################ CLUSTERING ############################
####################################################################

# http://stats.stackexchange.com/questions/124591/r-how-to-transform-the-similarity-matrix-to-distance-matrix-for-performing-hie
# https://rpubs.com/gaston/dendrograms
setwd(root2)

####### B1L
  temp = filter(d, set=="b1l") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_1_lower.txt", row.names = T, col.names = T, quote = F, sep="\t")  
    
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(MyScript = c("BACS1", "BACS1", "BACS1", "BACS1")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'MyScript', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-1 lowercase", xlab="", ylab="")  # Figure d1, 650x525

####### B1U
  temp = filter(d, set=="b1u") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_1_upper.txt", row.names = T, col.names = T, quote = F, sep="\t")  
  
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(MyScript = c("BACS1", "BACS1", "BACS1", "BACS1")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'MyScript', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-1 uppercase", xlab="", ylab="")  # Figure d2, 650x525

####### B2L
  temp = filter(d, set=="b2l") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_2_lowerSans.txt", row.names = T, col.names = T, quote = F, sep="\t")  
  
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(mmm = c("BACS2sans", "BACS2sans", "BACS2sans", "BACS2sans")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'mmm', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-2 Sans lowercase", xlab="", ylab="")  # Figure d4, 650x525


####### B2U
  temp = filter(d, set=="b2u") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs==1) %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_2_upperSans.txt", row.names = T, col.names = T, quote = F, sep="\t")  
  
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(mmm = c("BACS2sans", "BACS2sans", "BACS2sans", "BACS2sans")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'mmm', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-2 Sans uppercase", xlab="", ylab="")  # Figure d4, 650x525

####### B2LS
  temp = filter(d, set=="b2ls") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="A") %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_2_lowerSerif.txt", row.names = T, col.names = T, quote = F, sep="\t")  
  
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(mmm = c("BACS2serif", "BACS2serif", "BACS2serif", "BACS2serif")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'mmm', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-2 Serif lowercase", xlab="", ylab="")  # Figure d5, 650x525
  
####### B2US
  temp = filter(d, set=="b2us") %>% group_by(pair) %>% mutate(sim = mean(sim)) %>% filter(numPs=="VV") %>% data.frame()
  temp = temp %>% select(one, two, sim) %>% spread(two, value = sim)
  rownames(temp) = temp[,1]
  temp = temp[,-1]
  
  # export Appendix C
  write.table(round(temp, digits = 2), "simMatrix_BACS_2_upperSerif.txt", row.names = T, col.names = T, quote = F, sep="\t")  
  
  # dendrogram 
  hc = hclust(dist(temp))
  quartzFonts(mmm = c("BACS2serif", "BACS2serif", "BACS2serif", "BACS2serif")) # The first element of the vector is the normal face, then bold face, then italic face, then bold-italic font face. 
  par(family = 'mmm', cex=1.5)
  plot(hc, main="", xlab="", ylab="", sub="")
  par(family = 'Arial', cex=1)
  title(main="BACS-2 Serif uppercase", xlab="", ylab="")  # Figure d6, 650x525
  
