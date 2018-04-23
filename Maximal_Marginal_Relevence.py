import math
from nltk.tokenize import word_tokenize

def cos_sim(dict1,dict2):
    dict1_values=list(dict1.values())
    dict2_values=list(dict2.values())

    count1=0
    Sum=0

    while count1<len(dict1_values):
        Sum+=dict1_values[count1]*dict2_values[count1]
        count1+=1

    count2=0
    norm1=0
    while count2<len(dict1_values):
        norm1+=dict1_values[count2]**2
        count2+=1

    norm1=math.sqrt(norm1)

    count3=0
    norm2=0

    while count3<len(dict2_values):
        norm2+=dict2_values[count3]**2
        count3+=1

    norm2=math.sqrt(norm2)

    return Sum/(norm1*norm2)

##a={'shivam':1,'is':1,'good':1}
##b={'shivam':1,'is':0,'good':1}
##print(cos_sim(a,b))

def bag_of_words(dict1,sentence):
    dict2={}
    dict2=dict1
    words=word_tokenize(sentence)
    for each_word in words:
        if each_word in dict2:
            dict2[each_word]+=1
    return dict2

##dict1={'shivam':0,'satyam':0,'are':0,'brothers':0}
##sentence='satyam and shivam shivam are brothers'
##print(bag_of_words(dict1,sentence))


def MMR(sentence,title,narrative,arrSelected):
    ##sim1
    sim1=0
    bag={}
    title_words=word_tokenize(title)
    for each_word in title_words:
        if each_word not in bag:
            bag[each_word]=0

    narrative_words=word_tokenize(narrative)
    for each_word in narrative_words:
        if each_word not in bag:
            bag[each_word]=0

    query={}
    query=bag
    query=bag_of_words(query,sentence)
    topic={}
    topic=bag
    topic=bag_of_words(topic,title+" "+narrative)
    sim1= cos_sim(query,topic)

    ##sim2

    bag1={}

    for each_sent in arrSelected:
        sent_words=word_tokenize(each_sent)

        for each_word in sent_words:
            if each_word not in bag1:
                bag[each_word]=0

    sentence_words=word_tokenize(sentence)

    for each_word in sentence_words:
        if each_word not in bag1:
            bag1[each_word]=0

    query1={}
    query1=bag1
    query1=bag_of_words(query1,sentence)
    sim2=0
    for each_sent in arrSelected:
        vector_sent={}
        vector_sent=bag1
        vector_sent=bag_of_words(vector_sent,each_sent)
        cur_sim=cos_sim(query1,vector_sent)
        if cur_sim>sim2:
            sim2=cur_sim

    res=sim1-sim2
    return res


##arrSelected=['The man accused of killing Goa-based perfumer Monika Ghurde hid on the terrace of her apartment complex for two days before forcing his way into her flat — he abused and raped her, and finally smothered her with a pillow, the police said here on Tuesday','According to the police, the suspect — Rajkumar Singh, 21 — attacked Ghurde to avenge the humiliation and frustration of being thrown out of job']        
##print(MMR("He was arrested from Bengaluru on Sunday","Goa perfumer Monika Ghurde's murder","",arrSelected))


def final_summary(title,sentences):
    Score=[]
    for each_sent in sentences:
        Score.append(MMR(each_sent,title,"",""))

    return Score

## testing

text=open("murder.txt").read()
title=open("title.txt").read()

sentences=sent_tokenize(text)

print(final_summary(title,sentences))

    















    
