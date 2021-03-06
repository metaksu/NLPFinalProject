import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
import warnings
import spacy
from keras.preprocessing.text import Tokenizer

from kerasLSTM import KerasLSTMClassifier
from kerasGRU import KerasGRUClassifier
from kerasRNN import KerasRNNClassifier

warnings.filterwarnings('ignore')

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0],True)


def plotHistory(history, name="Model"):
    #  "Accuracy"
    plt.figure(name + " Accuracy")
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title(name + ' Accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')

    # "Loss"
    plt.figure(name + " Loss")
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title(name + ' Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')


hate_speech_corpus = pd.read_csv("hate_speech.csv")
hate_speech_corpus_final = hate_speech_corpus[['class', 'tweet']]

X = hate_speech_corpus_final[['tweet']]
y = hate_speech_corpus_final[['class']]
encoder = LabelEncoder()
y = encoder.fit_transform(y)
X = X.values
X = [x[0] for x in X]
plt.figure('Dataset Details')
sns.barplot(['Non Toxic', 'Toxic', 'Hate'], hate_speech_corpus_final['class'].map({0:"Non Toxic", 1: "Toxic", 2: "Hate"}).value_counts(), palette="icefire")
plt.title('Count of Toxic and Hate Comments of Dataset')

# !python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")

# Tokenizing & Vectorizing to create embeddings
tokenizer = Tokenizer(num_words=30000)
tokenizer.fit_on_texts(X)
embeddings_index = np.zeros((30000 + 1, 300))
for word, idx in tokenizer.word_index.items():
    try:
        embedding = nlp.vocab[word].vector
        embeddings_index[idx] = embedding
    except:
        pass

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=444, stratify=y)

lstmMODEL = KerasLSTMClassifier(emb_idx= embeddings_index)
print(lstmMODEL.model.summary())
h = lstmMODEL.fit(x_train, y_train)
print('\nLSTM Test Accuracy %.5f' % lstmMODEL.score(x_test, y_test))
plotHistory(h, "LSTM")

gru = KerasGRUClassifier()
h = gru.fit(x_train, y_train)
print('\nGRU Test Accuracy %.5f' % (gru.score(x_test, y_test)))
plotHistory(h, "GRU")

rnn = KerasRNNClassifier()
rnn.model.summary()
rnnFit = rnn.fit(x_train, y_train)
print('\nRNN Test Accuracy %.5f' % (rnn.score(x_test, y_test)))
plotHistory(rnnFit, "RNN")

plt.show()
