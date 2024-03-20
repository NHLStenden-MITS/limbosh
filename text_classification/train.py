# Script for training discriminative text classification models for prompt injection detection.
#
# Author: Saul Johnson <saul.johnson@nhlstenden.com>
# Usage: python3 train.py

from typing import Literal, Optional
import click
import joblib

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report, accuracy_score

import matplotlib.pyplot as plt
import pandas as pd


@click.command()
@click.option('--model', type=click.Choice(['nb', 'svm', 'rf', 'dummy']), default='nb', help='The type of model to train.')
@click.option('--cross-val', type=click.INT, default=5, help='Number of cross-validation folds to use.')
@click.option('--ngram-min', type=click.INT, default=1, help='The lower bound of the ngram range to use for training.')
@click.option('--ngram-max', type=click.INT, default=1, help='The upper bound of the ngram range to use for training.')
@click.option('--train', type=click.STRING, help='The training set to use.')
@click.option('--test', type=click.STRING, help='The testing set to use.')
@click.option('--output', type=click.STRING, help='The file in which to save the trained model.')
@click.option('--confusion-matrix-mode', type=click.Choice(['show', 'save', 'skip']), default='skip', help='What to do with the resulting confusion matrix.')
@click.option('--confusion-matrix-output', type=click.STRING, help='The file in which to save the rendered confusion matrix.')
def main(
    model: Literal['nb', 'svm', 'rf', 'dummy'],
    cross_val: int,
    ngram_min: int,
    ngram_max: int,
    train: str,
    test: str,
    output: Optional[str],
    confusion_matrix_mode: Literal['show', 'save', 'skip'],
    confusion_matrix_output: Optional[str]):
    """ The main function/entrypoint for the script.
    """
    # Load files in data directory, taking subdirectories as classes.
    # dataset = load_files('./data', load_content=True, encoding='UTF-8', decode_error='replace')

    # Split into testing and training data.
    # x_train, x_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.2) # 20% test data.

    training_dataset = pd.read_parquet(train)
    x_train = training_dataset['text']
    y_train = training_dataset['label']

    testing_dataset = pd.read_parquet(test)
    x_test = testing_dataset['text']
    y_test = testing_dataset['label']

    # Choose classifier depending on command-line args.
    classifier = MultinomialNB() # Multinomial Naive Bayes (default).
    if model == 'rf':
        classifier = SGDClassifier() # Linear SVM.
    if model == 'svm':
        classifier = RandomForestClassifier() # Random forest.
    if model == 'dummy':
        classifier = DummyClassifier() # Dummy classifier (for obtaining baseline).

    # Create pipeline.
    pipeline = Pipeline([('vectorizer', CountVectorizer(ngram_range=(ngram_min, ngram_max))), # Convert to token count matrix.
                        ('tfidf', TfidfTransformer()), # TFIDF normalization.
                        ('classifier', classifier)])

    # Actually train  model.
    pipeline.fit(x_train, y_train)

    # Put the model to the test.
    y_pred = pipeline.predict(x_test)

    # K-fold cross-validation.
    print('CROSS-VALIDATION ===============')
    print(cross_val_score(pipeline, x_train, y_train, cv=cross_val), '\n')

    # Confusion matrix, how many classification errors did we make?
    print('CONFUSION MATRIX ===============')
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    print(cm, '\n')

    # Classification report, what's our overall accuracy, support, F1 score and so on?
    print('CLASSIFICATION REPORT ==========')
    if model != 'dummy':
        print(classification_report(y_test, y_pred), '\n')
    else:
        print('No classification report available.\n')

    # What's our overall accuracy?
    print('OVERALL ACCURACY ===============')
    print(accuracy_score(y_test, y_pred), '\n')

    # Plot confusion matrix using matplotlib and either save or show it.
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipeline.classes_)
    disp.plot()
    if confusion_matrix_mode == 'show':
        plt.show()
    elif confusion_matrix_mode == 'save':
        plt.savefig(fname=confusion_matrix_output)

    # Pickle trained model to file for later use.
    joblib.dump(pipeline, output)


if __name__ == '__main__':
    main()
