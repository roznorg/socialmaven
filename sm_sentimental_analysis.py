import csv

import numpy as np
import pandas as pd

from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics import classification_report

from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC

from sm_settings import SMSettings

class SmSentimentalAnalysis:
    train_vectors = []
    train_data = []

    test_vectors = []
    test_data = []

    classifier = None
    features = None

    def __init__(self):
        n_estimators = 100

        self.classifier = OneVsRestClassifier(BaggingClassifier(LinearSVC(penalty="l1", dual=False), max_samples=1.0 / n_estimators, n_estimators=n_estimators), n_jobs=-1)
        self.features = self.get_features()
        self.set_train_test_data()
        self.set_classification_pipline()

    def get_features(self):
        vectorizer = {
            'tfid': TfidfVectorizer(min_df = 5,
                                 max_df = 0.8,
                                 sublinear_tf = True,
                                 use_idf = True),
        }

        return FeatureUnion([("tfid", vectorizer['tfid'])])

    def set_train_test_data(self):

        docs = pd.read_csv(SMSettings.datasets_root_path.format(SMSettings.default_lang) + SMSettings.training_dataset_name ,encoding="utf-8")
        msk = np.random.rand(len(docs["polarity"])) < 0.8
        self.train_data = docs["text"][msk]
        self.train_vectors = docs["polarity"][msk]

        self.test_data = docs["text"][~msk]
        self.test_vectors = docs["polarity"][~msk]



    def set_classification_pipline(self):
        pipeline = Pipeline([
                        ('features', self.features),
                        ('classifier', self.classifier)])
        pipeline.fit(self.train_data, self.train_vectors)
        pred = pipeline.predict(self.test_data)

        report = classification_report(self.test_vectors, pred, output_dict=True)
        print(report)


if __name__ == '__main__':
    sm_sentimental_analysis = SmSentimentalAnalysis()
