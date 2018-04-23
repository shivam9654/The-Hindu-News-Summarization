import nltk.data
import os
from nltk.tokenize import RegexpTokenizer ##for punctations
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize

def removePunctations(text):
    tokenizer = RegexpTokenizer(r'\w+')
    return  ' '.join(tokenizer.tokenize(text))

                     

def removeStopWords(words):
    stop_words=set(stopwords.words("english"))
    
    filtered_words=[]
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)
    
    return filtered_words



def getKeyWords(text):    ## return unique words from text and their counts in text
    text=removePunctations(text)
##    print(text)
    words =word_tokenize(text)
##    print(words)
    words= removeStopWords(words)
##    print(words)
    uniqueWords=list(set(words))
##    print(uniqueWords)
##    print(uniqueWords)
    keywords= [{'word': word,'count': words.count(word)} for word in uniqueWords]
    keywords=sorted(keywords,key=lambda x:-x['count'])
    

    return (keywords,len(words))


def getTopKeywords(text):
    (keywords,wordCount)= getKeyWords(text)
    for keyword in keywords:
        articleScore = keyword['count'] / wordCount
        keyword['totalScore'] = articleScore * 1.5
    return keywords


def SentencePositionScore(i,sentenceCount):

    
    PositionScore = i/(sentenceCount*1.0)

    if PositionScore >0 and PositionScore<= 0.1:
        return 0.17
    elif PositionScore > 0.1 and PositionScore <= 0.2:
        return 0.23
    elif PositionScore > 0.2 and PositionScore <= 0.3:
        return 0.14
    elif PositionScore > 0.3 and PositionScore <= 0.4:
        return 0.08
    elif PositionScore > 0.4 and PositionScore <= 0.5:
        return 0.05
    elif PositionScore > 0.5 and PositionScore <= 0.6:
        return 0.04
    elif PositionScore > 0.6 and PositionScore <= 0.7:
        return 0.06
    elif PositionScore > 0.7 and PositionScore <= 0.8:
        return 0.04
    elif PositionScore > 0.8 and PositionScore <= 0.9:
        return 0.04
    elif PositionScore > 0.9 and PositionScore <= 1.0:
        return 0.15
    else:
        return 0


def SentenceLengthScore(sentence,max_length):
    sent_words=word_tokenize(sentence)
    length=len(sent_words)
    return length/max_length
    




def TitleScore(titleWords, sentenceWords):
    matchedWords=[]
##    title_words=word_tokenize(title)
    titleWords=removeStopWords(titleWords)
##    sentence_words=word_tokenize(sentence)
    sentenceWords=removeStopWords(sentenceWords)
    matchedWords= [word for word in sentenceWords if word in titleWords]

    return (len(matchedWords)/len(titleWords)*1.0)









    
    








    
