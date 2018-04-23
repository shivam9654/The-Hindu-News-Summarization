import os
from Input import *
from preprocessing import *
from steeming import steemer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import numpy as np
import time
from Labeling import Label
import itertools
from generating import generate_summary
import csv


source=[]
summaries=[]
sentences=[]
summ_sentences=[]
Labels=[]
doc_lists=[] ##[[s1,s2,s3],[s4,s5,s6],]
doc_list=[]


sent_tfidfScore=[]
sent_titleScore=[]
sent_positionScore=[]
sent_lenScore=[]
sent_catScore=[]

train_data=[['tfidfScore','titleScore','positionScore','lenScore']]

path="C:/python/project/Dataset"

doc_path=path+'/set_A_text'
file_list=os.listdir(doc_path)

    

for i in range(len(file_list)):
    full_file_path=doc_path +'/'+file_list[i]
    source.append(open(full_file_path,'r').read())


summ_path=path+'/set_A_summaries'
summ_list=os.listdir(summ_path)


for i in range(len(summ_list)):
    full_summ_path=summ_path +'/'+summ_list[i]
    summaries.append(open(full_summ_path,'r').read())
    

titles=open("title.txt").readlines()


##print(len(summaries))
##print(len(source))

##print(len(file_list))
##print(summaries[0])

for i,each_doc in enumerate(source):
    doc=remove_agency_headers(each_doc)
    doc=remove_reported_said(doc)
    doc=according_to(doc)
    doc=remove_transcation(doc)
    doc=redundant_intros(doc)
    doc=age(doc)
    doc=days_of_week(doc)
    doc=remove_gmt(doc)
    doc=caps_opening(doc)
    doc=re.sub('--|AP|[()]|YORK|_',"",doc)
    source[i]=doc

##print(source[46])
##print(summaries[46])

for i,each_doc in enumerate(summaries):
    doc=remove_agency_headers(each_doc)
    doc=remove_reported_said(doc)
    doc=according_to(doc)
    doc=remove_transcation(doc)
    doc=redundant_intros(doc)
    doc=age(doc)
    doc=days_of_week(doc)
    doc=remove_gmt(doc)
    doc=caps_opening(doc)
    doc=re.sub('--|AP|[()]|YORK|_',"",doc)
    summaries[i]=doc
    


##label=Label(summaries[0],source[0])
##print(generate_summary(label,source[46]))

##for i,each_summ in enumerate(summaries):
##    label=Label(each_summ,source[i])
##    summary=generate_summary(label,source[i])
##    print(len(sent_tokenize(summary)))
##    print(len(sent_tokenize(each_summ)))
##    print("\n")

##print(summaries[45])


for each_doc in source: ##list of sentences ['s1','s2'.'s3']
    doc_sents= sent_tokenize(each_doc)
    doc_lists.append(doc_sents)
##    for each_sent in doc_sents:
##        sentences.append(each_sent)



for index,each_doc in enumerate(doc_lists):
    sentens=[]
    for each_doc_sent in each_doc:
        each_doc_sent=removePunctations(each_doc_sent.lower())
        doc_sent_words=word_tokenize(each_doc_sent)
        doc_sent_words=removeStopWords(doc_sent_words)
        doc_sent_words=steemer(doc_sent_words)
        sentence=' '.join(doc_sent_words)
        sentens.append(sentence)
        sentences.append(sentence)

    doc_list.append(sentens)


for each_doc in doc_list:
    max_l=[]
    for each_sent in each_doc:
        max_l.append(len(word_tokenize(each_sent)))
    max_length=max(max_l)
    for i in range(len(each_doc)):
        sent_lenScore.append(SentenceLengthScore(each_doc[i],max_length))

ab=8261
for i in range(7):
    print(sent_lenScore[ab+i])
    

##print(len(sentences))
##print(sentences[0])
        
##print(len(doc_list[1]))
##print(len(sentences))
##print(sentences[14100])
##sentences=list(filter(lambda sentence: sentence.strip(),sentences))
##print(sentences[14100])
##print(len(sentences))

##for index,each_sent in enumerate(sentences):
##    each_sent=removePunctations(each_sent.lower())
##    sent_words=word_tokenize(each_sent)
##    sent_words=removeStopWords(sent_words)
##    sent_words=steemer(sent_words)
##    
##    sentences[index]=' '.join(sent_words)

##print(sentences[14100])
##print(sentences[0])
##print(len(sentences))    



## calculating tf-idf


##vect = CountVectorizer()
##vect.fit(sentences)    ##Learn a list of words

##save_tf=open("tf.pickle","wb")
##pickle.dump(vect,save_tf)
##save_tf.close()

tf_pickle=open("tf.pickle","rb")           ##Remark1
vect=pickle.load(tf_pickle)

##print(len(vect.get_feature_names())) ##45,346

train_dtm=vect.transform(sentences) ##This is a 2d sparse array sentno in row and words  in column

##print(train_dtm.shape)  ##197040*45346

##tfidf = TfidfTransformer(norm="l2")
##tfidf.fit(train_dtm)
##print("IDF:", tfidf.idf_)

##save_tfidf=open("tfidf.pickle","wb")
##pickle.dump(tfidf,save_tfidf)
##save_tfidf.close()

tfidf_pickle=open("tfidf.pickle","rb")           ##Remark1
tfidf=pickle.load(tfidf_pickle)

tf_idf_matrix = tfidf.transform(train_dtm)

##print(tf_idf_matrix.toarray())
##print(tf_idf_matrix.shape)
##print(train_dtm.toarray())
##print(pd.DataFrame(train_dtm.toarray(),columns=vect.get_feature_names()))
##tfidf = TfidfTransformer(norm="l2")
##tfidf.fit(train_dtm)
##print("IDF",tfidf.idf_)

##print(tf_idf_matrix.shape)  
##print(tf_idf_matrix.nnz)
##print((tf_idf_matrix.nnz * tf_idf_matrix.dtype.itemsize) / 1e6)
##print(tf_idf_matrix.data / 1e6)
##print(tf_idf_matrix.shape[0] * tf_idf_matrix.shape[1] * tf_idf_matrix.dtype.itemsize / 1e6)



TF=tf_idf_matrix.astype(np.float32)
Tf_Idf=TF.toarray()
    
print("Before Tf.idf")
 
for index,each_TfIdf in enumerate(Tf_Idf):
    l=len(word_tokenize(sentences[index]))
    summ=0
    if l!=0:
        for i in each_TfIdf:
            summ+=i
        summ=summ/l
        
    sent_tfidfScore.append(summ)


##TF=train_dtm.astype(np.float32)
##Tf=TF.toarray()
##
##for i in range(10):
##    print(Tf_Idf[10])
##    
##print("Before Tf.idf")
## 
##for index,each_Tf in enumerate(Tf):
##    l=len(word_tokenize(sentences[index]))
##    summ=0
##
##    if l!=0:
##        for i in each_Tf:
##            summ+=i
##        summ=summ/l
##
##
##    sent_tfidfScore.append(summ)


print("After Tf.idf")


for each_doc,each_title in zip(doc_list,titles):
    each_title=removePunctations(each_title.lower())
    titleWords=word_tokenize(each_title)
    titleWords=removeStopWords(titleWords)
    titleWords=steemer(titleWords)

    for each_sent in each_doc:
        sentenceWords=word_tokenize(each_sent)
        sent_titleScore.append(TitleScore(titleWords,sentenceWords))

##print("length of titleScore is:",len(sent_titleScore))



for each_doc in doc_list:
    length=len(each_doc)
    for index,each_sent in enumerate(each_doc):
        sent_positionScore.append(SentencePositionScore(index+1,length))

##print(sent_positionScore[77])
##print(len(sent_positionScore))
##print(len(sent_tfidfScore))


    
## get all the Labels in the list [1,1,1,0,....,1,1,1]

##for each_summ,each_doc in zip(summaries,source):
##    label= Label(each_summ,each_doc)
##    for each_label in label:
##        Labels.append(each_label)  ##Labels is desired list
##
##
##save_labels=open("labels.pickle","wb")
##pickle.dump(Labels,save_labels)
##save_labels.close()


labels_pickle=open("labels.pickle","rb")           ##Remark1
Labels=pickle.load(labels_pickle)


##print(len(sentences))
##print(len(Labels))
    








##print("tfidf:",len(sent_tfidfScore),"title:",len(sent_titleScore),"position:",len(sent_positionScore),"length:",len(sent_lenScore))
##for i,j,k,l in zip(sent_tfidfScore,sent_titleScore,sent_positionScore,sent_lenScore):
##    train_data.append([i,j,k,l])
##
##print(len(train_data))
##
##with open("training.csv","w") as training_data:
##    trainfile_writer=csv.writer(training_data)
##
##    for each_list in train_data:
##        trainfile_writer.writerow(each_list)
##
##        
