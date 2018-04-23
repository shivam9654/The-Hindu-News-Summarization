import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn import preprocessing,cross_validation,neighbors,svm

## tfidfScore  titleScore  positionScore  lenScore

train = pd.read_csv('training.csv')

label_pickle=open("labels.pickle","rb")
labels=pickle.load(label_pickle)

X=train.loc[:]
##print(X.shape)
y=labels
##print(len(y))

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

clf=svm.SVC(kernel='linear',C=1,class_weight={1:35})
clf.fit(X_train,y_train)

save_classifier=open("clf.pickle","wb")
pickle.dump(clf,save_classifier)
save_classifier.close()

accuracy=clf.score(X_test,y_test)
print("Accuracy of the classifier:--",accuracy)




##sns.pairplot(data,x_vars=['titleScore','positionScore','lenScore'],y_vars=)

##data.plot()
##plt.plot(data['tfidfScore'])
##plt.show()


##print(data.head())
##print(data.tail())
##print(data.shape)


