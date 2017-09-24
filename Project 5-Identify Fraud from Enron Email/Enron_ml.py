#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from tabulate import tabulate
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import precision_score, recall_score
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

### Task 1: Select what features you'll 'from_poi_to_this_person'use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances',
                      'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                      'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                      'restricted_stock', 'director_fees']
email_features = ['to_messages', 'email_address', 'from_poi_to_this_person', 'from_messages',
                  'from_this_person_to_poi', 'shared_receipt_with_poi']
email_features_num = ['to_messages', 'from_poi_to_this_person', 'from_messages',
                      'from_this_person_to_poi', 'shared_receipt_with_poi']
selected_financial_features = ['salary', 'total_payments', 'bonus', 'total_stock_value',
                               'expenses', 'exercised_stock_options', 'long_term_incentive']

features_list = ['poi'] # You will need to use more features
features_list.extend(financial_features)
features_list.extend(email_features_num)
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

data = featureFormat(data_dict, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

#################################
### Data Exploration POI
#################################
print 'Data Exporation'
print 'Number of data points: ', len(labels)
print 'Number of POI: ', labels.count(1)
print 'Number of Non-POI, ', labels.count(0)
print 'Percentage POI: ', 1.0 * labels.count(1) / len(labels)
print 'Percentage non-POI: ', 1.0 * labels.count(0) / len(labels)

num_poi = labels.count(1)
num_non_poi = labels.count(0)
# missing values in financial features
missing_data_list = []
for i in range(len(financial_features)):
    missing_value_count_poi = 0
    missing_value_count_non_poi = 0
    for j in range(len(features)):
        if features[j][i] == 0 and labels[j] == 1:
            missing_value_count_poi += 1
        elif features[j][i] == 0 and labels[j] == 0:
            missing_value_count_non_poi += 1
    total_missing = missing_value_count_poi + missing_value_count_non_poi
    poi_missing_perc = 1.0 * missing_value_count_poi / num_poi
    non_poi_missing_perc = 1.0 * missing_value_count_non_poi / num_non_poi
    missing_data_list.append([financial_features[i], total_missing, poi_missing_perc, non_poi_missing_perc])

print tabulate(missing_data_list, headers = ['Missing Num', 'POI Percentage', 'Non-POI Percentage'])

#################################
### Task 2: Remove outliers
#################################
data_dict.pop("TOTAL", 0) #
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)
data_dict.pop('LOCKHART EUGENE E',0)


#################################
### Task 3: Create new feature(s)
#################################
for name in data_dict:
    if data_dict[name]['from_poi_to_this_person']!='NaN' and data_dict[name]['to_messages']!='NaN' and data_dict[name]['to_messages']!=0:
        data_dict[name]['from_poi_rate'] = data_dict[name]['from_poi_to_this_person']/data_dict[name]['to_messages']
    else:
        data_dict[name]['from_poi_rate'] = 'NaN'

    if data_dict[name]['from_this_person_to_poi']!='NaN' and data_dict[name]['from_messages']!='NaN' and data_dict[name]['from_messages']!=0:
        data_dict[name]['to_poi_rate'] = data_dict[name]['from_this_person_to_poi']/data_dict[name]['from_messages']
    else:
        data_dict[name]['to_poi_rate'] = 'NaN'

    if data_dict[name]['bonus']!='NaN' and data_dict[name]['salary']!='NaN' and data_dict[name]['salary']!=0:
        data_dict[name]['bonus_to_salary'] = data_dict[name]['bonus']/data_dict[name]['salary']
    else:
        data_dict[name]['bonus_to_salary'] = 'NaN'

    if data_dict[name]['total_stock_value']!='NaN' and data_dict[name]['salary']!='NaN' and data_dict[name]['salary']!=0:
        data_dict[name]['stock_to_salary'] = data_dict[name]['total_stock_value']/data_dict[name]['salary']
    else:
        data_dict[name]['stock_to_salary'] = 'NaN'

features_list.extend(['from_poi_rate', 'to_poi_rate', 'bonus_to_salary', 'stock_to_salary'])
my_dataset = data_dict

from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)
scaler = preprocessing.MinMaxScaler()
features = MinMaxScaler().fit_transform(features)

#k best
def get_k_best(features_list, k):
    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_

    unsorted_pairs = zip(features_list[1:], scores)
    #print unsorted_pairs
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    #print sorted_pairs
    k_best_features = dict(sorted_pairs[1:k+1])
    #k_best_features = dict(sorted_pairs[:k])
    return k_best_features.keys()

kbest_features_list=get_k_best(features_list,5)# select the top ten features according to their k score.
kbest_features_list.insert(0, 'poi')
#print kbest_features_list
features_list = kbest_features_list

data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)


#print features
### Task 4: Try a varity of classifiers

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Create Classifier

from sklearn.cross_validation import StratifiedShuffleSplit

# Decision Tree
#clf = tree.DecisionTreeClassifier()
#param_grid = dict(
#criterion=['gini', 'entropy'],
#max_depth=[None, 1, 2, 3,4,5],
#min_samples_split=[1,2,3,4],
#class_weight=[None, 'balanced'],
#min_samples_leaf=[1,2,3,4,5],
#min_weight_fraction_leaf=[0.05,0.1,0.2,0.3])
#sss = StratifiedShuffleSplit(labels)
#rf_search = GridSearchCV(clf, param_grid, cv=sss, scoring="f1")
#clf = clf.fit(features, labels)

# GaussianNB
clf = GaussianNB()
clf = clf.fit(features_train, labels_train)


# Create Accuracy
score = clf.score(features_test, labels_test)
predictions = clf.predict(features_test)
# Recall & Precision
recall = recall_score(labels_test, predictions)
precision = precision_score(labels_test, predictions)

print 'recall score: ', recall
print 'precision score: ', precision

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)