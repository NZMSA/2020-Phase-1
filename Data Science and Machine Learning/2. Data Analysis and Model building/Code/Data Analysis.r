---
title: "MSA-2020"
author: "Xuanyi Wang - xwan@aucklanduni.ac.nz"
date: "6/21/2020"
output: pdf_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## Data Exploration
```{r}
#load dataset
library(readr)
housePrice <- read_csv("Documents/housePrice.csv")
#explore the dataset
summary(housePrice)
#convert variable type
housePrice$`Land area` = sub(" .*", "", housePrice$`Land area`)
housePrice$`Land area` = as.numeric(housePrice$`Land area`)
```

## Correlation plots
```{r echo=FALSE, fig.height=7, fig.width=7}
pairs(housePrice[,-2],pch=19,col=rgb(0,0,1,.4))
#keep only key variables in the plot
pairs(housePrice[,-c(2,6:9,11:16)],pch=19,col=rgb(0,0,1,.4))
```

## Fit models
```{r echo=FALSE, fig.height=7, fig.width=7}
#exclude address from dataset
modelset = housePrice[,-2]
summary(modelset)
#basic full model
model1=lm(CV~.,data=modelset)
summary(model1)

#log model
model2=lm(log(CV)~.,data=modelset)
summary(model2)

#select some key variables
modelset3 = modelset[,-c(5:7)]
model3=lm(log(CV) ~ . ,data=modelset3)
summary(model3)
```

```{r}
library(readr)
housePrice2 <- read_csv("Downloads/dataset (1).csv")
```

```{r echo=FALSE, fig.height=7, fig.width=7}
#exclude address from dataset
modelset = housePrice2[,-3]
summary(modelset)
#basic full model
model1=lm(CV~.,data=modelset)
summary(model1)

#log model
model2=lm(log(CV)~.,data=modelset)
summary(model2)

#select some key variables
modelset3 = modelset[,-c(5:7)]
model3=lm(log(CV) ~ . ,data=modelset3)
summary(model3)
```
