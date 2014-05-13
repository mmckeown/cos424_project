
# read in csv files
bagofwords = read.csv('~/cos424_project/sample_data_100/bag_of_words.csv', header=T, row.names=1)
attribs = read.csv('~/cos424_project/data/rand_1000/attributes.csv', header=T, row.names=1)

# calculate ratios of pos/neg words to total words
attribs$pos_ratio = attribs$pos_count/attribs$word_count
attribs$neg_ratio = attribs$neg_count/attribs$word_count
attribs$posneg_ratio = attribs$pos_count/attribs$neg_count

mean(attribs$pos_ratio,na.rm=T)

# rank unis by different statistics. Calculate stddev of ratio. This gives param estimates for simple gaussian model
pos_aggs = aggregate(attribs[['pos_ratio']], by=list(attribs[['University.institution']]), FUN=function(x){mean(x,na.rm=T)})
pos_aggs2 = aggregate(attribs[['pos_ratio']], by=list(attribs[['University.institution']]), FUN=function(x){sd(x,na.rm=T)})
colnames(pos_aggs) = c('University','pos_ratio')
pos_aggs$std_dev = pos_aggs2$x
pos_aggs = pos_aggs[with(pos_aggs, order(-pos_ratio, University)), ]
rownames(pos_aggs) = pos_aggs$University
pos_aggs$University = NULL

# 
pos_aggs = aggregate(attribs[['pos_ratio']], by=list(attribs[['University.location']]), FUN=function(x){mean(x,na.rm=T)})
pos_aggs2 = aggregate(attribs[['pos_ratio']], by=list(attribs[['University.location']]), FUN=function(x){sd(x,na.rm=T)})
colnames(pos_aggs) = c('Location','pos_ratio')
pos_aggs$std_dev = pos_aggs2$x
pos_aggs = pos_aggs[with(pos_aggs, order(-pos_ratio, Location)), ]

temp = pos_aggs
temp$std_dev = NULL
temp = na.omit(temp)
temp$quartile <- with(temp, cut(pos_ratio, 
                                breaks=quantile(pos_ratio, probs=seq(0,1, by=0.25),na.rm=T), 
                                include.lowest=TRUE,
                                labels=1:4))

neg_aggs = aggregate(attribs[['neg_ratio']], by=list(attribs[['University.institution']]), FUN=mean)
neg_aggs2 = aggregate(attribs[['neg_ratio']], by=list(attribs[['University.institution']]), FUN=sd)
colnames(neg_aggs) = c('University','neg_ratio')
neg_aggs$std_dev = neg_aggs2$x
neg_aggs = neg_aggs[with(neg_aggs, order(-neg_ratio, University)), ]

posneg_aggs = aggregate(attribs[['posneg_ratio']], by=list(attribs[['University.institution']]), FUN=mean)
colnames(posneg_aggs) = c('University','posneg_ratio')
posneg_aggs = posneg_aggs[with(posneg_aggs, order(-posneg_ratio, University)), ]

# 

page_aggs = aggregate(attribs[['Number.of.pages']], by=list(attribs[['University.institution']]), FUN=mean)
page_aggs2 = aggregate(attribs[['Number.of.pages']], by=list(attribs[['University.institution']]), FUN=sd)
colnames(page_aggs) = c('University','Number.of.pages')
rownames(page_aggs) = page_aggs$University
page_aggs$University = NULL
page_aggs$std_dev = page_aggs2$x
page_aggs = page_aggs[with(page_aggs, order(-Number.of.pages, University)), ]

hist(attribs$word_count, col='lavender', main="Acknowledgement lengths", xlab="Number of words")



# ldavocab = names(bagofwords)
# docnames = rownames(bagofwords)
# 
# ldadocs = list()
# for (i in 1:length(docnames)){
#   ldadocs = append(ldadocs,NA)
# }
# for (i in 1:length(docnames)){
#   vocab_indices = which(as.vector(bagofwords[i,])!=0)
#   #matrix = as.matrix(rbind(1:length(bagofwords[1,]),bagofwords[1,]))
#   matrix = as.matrix(rbind(vocab_indices,as.vector(bagofwords[i,vocab_indices])))
#   if(length(matrix)>0){
#     ldadocs[[i]] = matrix
#   }
# }
# for (i in length(docnames):1){
#   if(is.na(ldadocs[[i]])){
#     ldadocs[[i]] = NULL
#   }
# }
# 
# lda.collapsed.gibbs.sampler(ldadocs,5,ldavocab,3,0.5,0.3)
