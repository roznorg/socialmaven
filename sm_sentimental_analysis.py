import csv

import pandas as pd

from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC

from libs.vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sm_settings import SMSettings

class SmSentimentalAnalysis:
    train_vectors = []
    train_data = []

    test_vectors = []
    test_data = []

    classifier = None
    features = None

    def __init__(self):
        n_estimators = 10
        self.classifier = OneVsRestClassifier(BaggingClassifier(LinearSVC(penalty="l1", dual=False), max_samples=1.0 / n_estimators, n_estimators=n_estimators), n_jobs=-1)
        self.vectorizer = TfidfVectorizer(min_df = 5,
                             max_df = 0.8,
                             sublinear_tf = True,
                             use_idf = True)
        self.set_train_test_data()
        self.set_classification_pipline()


    def set_train_test_data(self):

        docs = pd.read_csv(SMSettings.paths['datasets_root_path'].format(SMSettings.default_lang) + SMSettings.training_dataset_name ,encoding="utf-8")
        msk = np.random.rand(len(docs["polarity"])) < 0.8
        self.train_data_content = docs["text"][msk]
        self.train_data_label = docs["polarity"][msk]

        docs_test = pd.read_csv(SMSettings.paths['datasets_root_path'].format(SMSettings.default_lang) + SMSettings.test_dataset_name ,encoding="utf-8")
        msk_test = np.random.rand(len(docs_test["polarity"])) < 0.2

        self.test_data_content = docs_test["text"][msk_test]
        self.test_data_label = docs_test["polarity"][msk_test]

        self.train_vectors = self.vectorizer.fit_transform(self.train_data_content)
        self.test_vectors = self.vectorizer.transform(self.test_data_content)



    def set_classification_pipline(self):
        self.classifier.fit(self.train_vectors, self.train_data_label)
        pred = self.classifier.predict(self.test_vectors)
        analyser = SentimentIntensityAnalyzer()

        for idx, input, prediction, label in zip(enumerate(self.test_data_content), self.test_data_content, pred, self.test_data_label):
            print(analyser.polarity_scores(input))
            print("No.", idx[0], 'input,',input, ', has been classified as', prediction, 'and should be', label)

        report = classification_report(self.test_data_label, pred, output_dict=True)
        print(report)


if __name__ == '__main__':
    sm_sentimental_analysis = SmSentimentalAnalysis()
