import os
from Input import *
from preprocessing import *
from steeming import steemer
from preprocessing import summary
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import numpy as np
import time
from Labeling import Label
import itertools
from generating import generate_summary
import csv
from numpy import count_nonzero

 
doc=open("murder.txt").read()
title=open("title.txt").read()

sentences=sent_tokenize(doc)
print("No of sentences in document:-",len(sentences)+5)

def summly(doc,title):

    sentencearray=[]
    sent_tfidf=[]
    sent_title=[]
    sent_position=[]
    sent_len=[]
    test_data=[]

    sentences=sent_tokenize(doc)
    
    for each_sent in sentences:
        
        each_sent=removePunctations(each_sent.lower())
        sent_words=word_tokenize(each_sent)
        sent_words=removeStopWords(sent_words)
        sent_words=steemer(sent_words)
        sentence=' '.join(sent_words)
        sentencearray.append(sentence)


    tf_pickle=open("tf.pickle","rb")        
    vect=pickle.load(tf_pickle)



    test_dtm=vect.transform(sentencearray)

    tfidf_pickle=open("tfidf.pickle","rb")          
    tfidf=pickle.load(tfidf_pickle)

    tf_idf_matrix=tfidf.transform(test_dtm)

    TF=tf_idf_matrix.astype(np.float32) 

    Tf_Idf=TF.toarray()

    

    for index,each_TfIdf in enumerate(Tf_Idf):
        l=len(word_tokenize(sentencearray[index]))
        summ=0
        if l!=0:
            for i in each_TfIdf:
                summ+=i
            summ=summ/l

        sent_tfidf.append(summ)


    title=removePunctations(title.lower())
    titleWords=word_tokenize(title)
    titleWords=removeStopWords(titleWords)
    titleWords=steemer(titleWords)

    for each_sent in sentencearray:
        sentenceWords=word_tokenize(each_sent)
        sent_title.append(TitleScore(titleWords,sentenceWords))




    length=len(sentencearray)
    for index,each_sent in enumerate(sentencearray):
        sent_position.append(SentencePositionScore(index+1,length))


    max_l=[]
    for each_sent in sentencearray:
        max_l.append(len(word_tokenize(each_sent)))
        
    max_length=max(max_l)
    

    for i in range(len(sentencearray)):
        sent_len.append(SentenceLengthScore(sentencearray[i],max_length))


    

    for i,j,k,l in zip(sent_tfidf,sent_title,sent_position,sent_len):
        test_data.append([i,j,k,l])

    


    classifier_pickle=open("clf.pickle","rb")
    clf=pickle.load(classifier_pickle)

    prediction=clf.predict(test_data)
    countt=count_nonzero(prediction)
    l=len(sent_tokenize(doc))
    if countt>=3: 
        return generate_summary(prediction,doc)
    else:
        print("text teaser")
        return summary(doc,title)
        


summary=summly(doc,title)
sentencess=sent_tokenize(summary)

print("No of sentence in summary:-",len(sentencess))
print("\n\n")

print(summary)





