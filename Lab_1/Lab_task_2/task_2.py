#space for task 2
'''
1 . In the initial task, the data is endowed with labels, signifying a supervised learning approach for Task
2. To proceed, it is imperative to carry out classification based on the information acquired in Task
1. Before delving into the classification process, it is crucial to preprocess the gathered data,
thoroughly scrutinizing for any potential missing values, null entries, or redundant data.
2. Subsequent to the preprocessing step, the dataset needs to be partitioned into distinct training and
testing subsets. Following this, the data should undergo a standardization process, for instance,
employing a technique such as standardization, to ensure uniformity across the dataset.
3. Once the scaling process is completed, the subsequent phase involves the implementation of
suitable machine-learning algorithms to conduct the classification task.
4. Upon the completion of the training phase, it is imperative to evaluate the model's efficacy by
subjecting it to the designated testing set. This evaluation process should culminate in the
generation of a comprehensive performance report, encompassing various accuracy metrics for
thorough analysis.
5. To conclude the process, it is recommended to save the trained model, facilitating its seamless
deployment for future applications.


'''

# 
# TODO split based on data loading and preprocessing, model training, and
    
    
#load class
import numpy as np
import pandas as pd 

'''in case it's not installed then install using conda create


-c conda-forge -n name_of_my_env python pandas
# more installations information can be found:
https://pandas.pydata.org/docs/getting_started/install.html'''

import os
#load sklearn module for creating and evaluating ML models. In case sklearn isn't installed,
#follow this link https://scikit-learn.org/stable/install.html for further details on the installation process.

from sklearn.neighbors import KNeighborsClassifier 

'''#load your classifier. In this
code, I have used KNN. You can choose other algorithms. You have to use at least
3 to complete this.'''

from sklearn.preprocessing import StandardScaler #module for perform scaling

from sklearn.model_selection import train_test_split #module for splitting datatset
from sklearn import metrics #module for evaluating performance

#load your data
df = pd.read_csv("data.csv") #change the name accordingly
df.head() # prints top 5 rows from the datatset to check data is load or not


# Check for missing values
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values)
      
#remove duplicates
df = df.drop_duplicates()

# TODO data preprocessing up to here, separate from model training in ipynb.

# prepare features
x = df.drop(['Label'],axis=1) #remove class or label
y = df['Label'] #load label

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=.2) 
#split datatset. Here ratio is 80:20. Change accordingly

# Scale the data using standardization
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train) #scale training set
x_test = scaler.transform(x_test) #scale test set

z = KNeighborsClassifier(n_neighbors=3) # KNN classifier for 3 neighbours
KNN = z.fit(x_train,y_train) # start training

predict = KNN.predict(x_test) # performance in the test set

print("Accuracy:", metrics.accuracy_score(y_test,predict)) # evaluating the performance based on accuracy


## TODO move to ipynb: part that stores the model

#library for save and load scikit-learn models

import pickle
# file name, recommending *.pickle as a file extension
filename = "model.pickle"

# save model
pickle.dump(z, open(filename, "wb"))