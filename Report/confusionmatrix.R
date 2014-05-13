install.packages("e1071")
library(e1071)


bagofwordsivy <- read.csv("bag_of_words_ivy.csv", header = T)
bagofwordsrand<- read.csv("bag_of_words_rand.csv", header = T)
bagofwords <- read.csv("bag_of_words.csv", header = T)
View(bagofwords)
View(bagofwordsrand)
View(bagofwordsivy)
attrs <- read.csv("attributes.csv", header = T)
attrsrand <- read.csv("attributes_rand.csv", header = T)
attrsivy <- read.csv("attributes_ivy.csv", header = T)
View(attrs)
View(attrsrand)
View(attrsivy)

namelocation <- levels(attrs$University.location)
for(i in 1:nrow(attrs)) {
  o <- attrs$University.location[i] == namelocation
  print(which(o==TRUE))
  print(i)
  attrs$locationnumber[i] <- which(o==TRUE)
}
namelocationrand <- levels(attrsrand$University.location)
for(i in 1:nrow(attrsrand)) {
  o <- attrsrand$University.location[i] == namelocationrand
  print(which(o==TRUE))
  print(i)
  attrsrand$locationnumber[i] <- which(o==TRUE)
}
namelocationivy <- levels(attrsivy$University.location)
for(i in 1:nrow(attrsivy)) {
  o <- attrsivy$University.location[i] == namelocationivy
  print(which(o==TRUE))
  print(i)
  attrsivy$locationnumber[i] <- which(o==TRUE)
}

universityname = levels(attrsivy$University.institution)
for(i in 1:nrow(attrsivy)) {
  o <- attrsivy$University.institution[i] == universityname 
  print(which(o==TRUE))
  print(i)
  attrsivy$universitynumber[i] <- which(o==TRUE)
}

Dep = levels(attrsivy$Department)
Depname 

for(i in 1:nrow(attrsivy)) {
  o <- attrsivy$Department[i] == Dep
  print(which(o==TRUE))
  print(i)
  attrsivy$universityDepnum[i] <- Depname[which(o==TRUE)]
}

IvyUnive = as.numeric(subset(attrsivy$universitynumber, !attrsivy$word_count==0))
IvyWordcount =  as.numeric(subset(attrsivy$word_count, !attrsivy$word_count==0))
IvyPoscount =  as.numeric(subset(attrsivy$pos_count, !attrsivy$word_count==0))
IvyNegcount =  as.numeric(subset(attrsivy$neg_count, !attrsivy$word_count==0))
IvyField =  as.numeric(subset(attrsivy$universityDepnum, !attrsivy$word_count==0))
RatioIvyPosWord=IvyPoscount/IvyWordcount
Rq = quantile(RatioIvyPosWord) 
RatioIvyPosWord <=Rq[1]
Y = RatioIvyPosWord 
Y[which(RatioIvyPosWord >=median(RatioIvyPosWord))]=1
Y[which(!Y==1)]=0
MatrixIvy = as.data.frame(cbind(IvyWordcount, IvyUnive, IvyNegcount, IvyField, Y))

test.train <- function(df, ntest)
{
  test.idx <- sort(sample(dim(df)[1], ntest, replace=F))
  test <- df[test.idx,]
  train <- df[-test.idx,]
  list(train=train, test=test)
}
NumTest = round(nrow(MatrixIvy) * 0.3)
Bundle <- test.train(MatrixIvy, ntest=NumTest)
MatrixIvyTraining <- data.frame(Bundle$train)
MatrixIvyTesting <- data.frame(Bundle$test)

model <- naiveBayes(as.factor(Y) ~ ., data=MatrixIvyTraining)
conf <- table(predict(model, MatrixIvyTesting[,-5]), MatrixIvyTesting[,5], dnn=list('predicted', 'actual'))

conf <- aaply(conf, 1, function(x) x / sum(x))
acc <- sum(diag(conf)) / sum(conf)

# Plot confusion matrix
plot.confusion <- function(conf)
{
  melted <- melt(conf, c("predicted", "actual"))
  p <- ggplot(data=melted, aes(x=predicted, y=actual, size=value))
  p <- p + geom_point(shape=15)
  #  p <- p + scale_size_area(to=c(1,20))
  p <- p + theme_bw() + theme(axis.text.x = element_text(angle=90))
  p
}
plot.confusion(conf)

table(predict(classifier, MatrixIvy), Y, dnn=list('predicted','actual'))

classifier<-naiveBayes(iris[,1:4], iris[,5]) 
table(predict(classifier, iris[,-5]), iris[,5], dnn=list('predicted','actual'))


Y[which(RatioIvyPosWord >Rq[1] && RatioIvyPosWord<=Rq[2])]=2
Y[which(RatioIvyPosWord >Rq[2] && RatioIvyPosWord<=Rq[3])]=3
Y[which(RatioIvyPosWord >Rq[3] && RatioIvyPosWord<=Rq[4])]=4

classifier <- naiveBayes(MatrixIvy,IvyPoscount)
table(predict(classifier, MatrixIvy), IvyPoscount, dnn=list('predicted','actual'))


classifier <- naiveBayes(MatrixIvy[1:900 ,],IvyPoscount[1:900])
table(predict(classifier, MatrixIvy[901:length(IvyPoscount) ,]), IvyPoscount[901:length(IvyPoscount) ], dnn=list('predicted','actual'))


classifier<-naiveBayes(iris[,1:4], iris[,5]) 
table(predict(classifier, iris[,-5]), iris[,5], dnn=list('predicted','actual'))


classifier<-naiveBayes(iris[,1:4], iris[,5]) 
table(predict(classifier, iris[,-5]), iris[,5], dnn=list('predicted','actual'))



